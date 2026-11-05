const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(__dirname + '/analytics.js', 'utf8');

class Events {
  listeners = {};
  addEventListener(name, fn, options = {}) {
    (this.listeners[name] ||= []).push({ fn, once: options.once });
  }
  fire(name, event = {}) {
    const listeners = this.listeners[name] || [];
    this.listeners[name] = listeners.filter((entry) => !entry.once);
    for (const { fn } of listeners) fn(event);
  }
}

function setup(url = 'http://localhost/?utm_source=linkedin&utm_medium=social&utm_campaign=always_on') {
  const form = new Events();
  const video = Object.assign(new Events(), {
    dataset: { analyticsVideo: 'cub-pipetting' }, currentTime: 0, duration: 4,
    paused: false, seeking: false, autoplay: true,
  });
  const observers = [];
  class Observer {
    targets = new Set();
    constructor(callback) { this.callback = callback; observers.push(this); }
    observe(target) { this.targets.add(target); }
    unobserve(target) { this.targets.delete(target); }
    show(target, ratio = 1) {
      if (this.targets.has(target)) this.callback([{ target, isIntersecting: true, intersectionRatio: ratio }]);
    }
  }
  const heading = { closest: () => ({ id: 'compare' }) };
  const scripts = [];
  const document = Object.assign(new Events(), {
    referrer: 'https://www.linkedin.com/feed/?private=excluded', hidden: false,
    head: { append: (script) => scripts.push(script) }, createElement: () => ({}),
    getElementById: () => form,
    querySelectorAll: (selector) => selector.startsWith('video') ? [video] : [heading],
  });
  const window = { IntersectionObserver: Observer };
  const context = vm.createContext({ window, document, location: new URL(url), URL, URLSearchParams, IntersectionObserver: Observer });
  vm.runInContext(source, context);
  const events = (name) => window.dataLayer.filter((entry) => entry[0] === 'event' && (!name || entry[1] === name));
  const click = (href, section = 'instruments') => {
    const link = { href, closest: (selector) => selector === 'section[id]' ? { id: section } : null };
    document.fire('click', { target: { closest: () => link } });
  };
  return { window, document, form, video, heading, scripts, observers, context, events, click };
}

test('retains UTM attribution, removes private queries, and keeps previews out of GA4', () => {
  const env = setup('http://localhost/?utm_source=linkedin&utm_medium=social&utm_campaign=always_on&email=private@example.com&utm_content=private@example.com');
  const config = env.window.dataLayer.find((entry) => entry[0] === 'config')[2];
  assert.match(config.page_location, /utm_source=linkedin/);
  assert.doesNotMatch(config.page_location, /private|email/);
  assert.equal(config.page_referrer, 'https://www.linkedin.com/feed/');
  assert.equal(env.scripts.length, 0);
});

test('production loads the existing GA4 property exactly once', () => {
  const env = setup('https://www.ursalabs.ai/?utm_source=substack&utm_medium=email&utm_campaign=always_on');
  vm.runInContext(source, env.context);
  assert.equal(env.scripts.length, 1);
  assert.match(env.scripts[0].src, /G-CFM3B0DT2P$/);
  assert.equal(env.window.dataLayer.filter((entry) => entry[0] === 'config').length, 1);
});

test('contact intent and resource events contain placement without private mailto contents', () => {
  const env = setup();
  env.click('http://localhost/#airtable');
  env.click('mailto:alex@ursalabs.ai?body=private-message');
  env.click('https://github.com/Hydra-Laboratories/CubOS?secret=private-value');
  assert.equal(env.events('contact_cta_click')[0][2].section_id, 'instruments');
  assert.equal(env.events('email_click').length, 1);
  assert.equal(env.events('resource_click')[0][2].link_path, '/Hydra-Laboratories/CubOS');
  assert.doesNotMatch(JSON.stringify(env.events()), /private|secret|mailto|alex@/);
});

test('form start fires once and email draft is never reported as a confirmed lead', () => {
  const env = setup();
  env.form.fire('input', { target: { value: 'private@example.com' } });
  env.form.fire('input', { target: { value: 'private message' } });
  env.document.fire('ursa:contact-draft-open');
  assert.equal(env.events('contact_form_start').length, 1);
  assert.equal(env.events('contact_email_draft_open').length, 1);
  assert.equal(env.events('generate_lead').length, 0);
  assert.doesNotMatch(JSON.stringify(env.events()), /private/);
});

test('section views deduplicate and do not fire below the visibility threshold', () => {
  const env = setup();
  env.observers[0].show(env.heading, 0.2);
  assert.equal(env.events('section_view').length, 0);
  env.observers[0].show(env.heading);
  env.observers[0].show(env.heading);
  assert.equal(env.events('section_view').length, 1);
});

test('contact handler only reports valid draft attempts and never shares form data with analytics', () => {
  const env = setup();
  let valid = false;
  env.form.reportValidity = () => valid;
  const status = {};
  env.document.getElementById = (id) => id === 'contact-form' ? env.form : status;
  env.document.dispatchEvent = (event) => env.document.fire(event.type);
  env.context.CustomEvent = class { constructor(type) { this.type = type; } };
  env.context.FormData = class {
    get(name) { return ({ name: 'Test User', email: 'private@example.com', organization: 'Test Lab', message: 'Private inquiry', interest: 'Collaboration' })[name]; }
  };
  env.window.location = { href: '' };
  vm.runInContext(fs.readFileSync(__dirname + '/contact.js', 'utf8'), env.context);
  env.form.fire('submit', { preventDefault() {} });
  assert.equal(env.events('contact_email_draft_open').length, 0);
  valid = true;
  env.form.fire('submit', { preventDefault() {} });
  assert.equal(env.events('contact_email_draft_open').length, 1);
  assert.match(env.window.location.href, /^mailto:alex@ursalabs.ai\?subject=/);
  assert.doesNotMatch(JSON.stringify(env.events()), /Private|private|Test User|Test Lab/);
  assert.equal(status.hidden, false);
});

test('demo counts visible playback once across loops; seeking and hidden playback do not count', () => {
  const env = setup();
  const tick = (time) => { env.video.currentTime = time; env.video.fire('timeupdate'); };
  tick(1);
  assert.equal(env.events('demo_video_start').length, 0);
  env.observers[1].show(env.video);
  env.video.currentTime = 3;
  env.video.fire('seeking');
  tick(3);
  assert.equal(env.events('demo_video_progress').length, 0);
  env.document.hidden = true;
  tick(3.5);
  env.document.hidden = false;
  tick(0);
  for (let loop = 0; loop < 3; loop++) {
    for (let time = 0.5; time <= 4; time += 0.5) tick(time);
    tick(0);
  }
  assert.equal(env.events('demo_video_start').length, 1);
  assert.deepEqual(Array.from(env.events('demo_video_progress'), (entry) => entry[2].video_percent), [25, 50, 75]);
  assert.equal(env.events('demo_video_complete').length, 1);
});
