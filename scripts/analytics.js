(() => {
  'use strict';
  if (window.ursaAnalytics) return;

  const measurementId = 'G-CFM3B0DT2P';
  const production = ['www.ursalabs.ai', 'ursalabs.ai'].includes(location.hostname);
  const query = new URLSearchParams(location.search);
  const campaignKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'utm_id', 'utm_source_platform'];

  // Keep campaign attribution while excluding arbitrary queries and form data.
  const pageUrl = new URL(location.pathname, location.origin);
  for (const key of campaignKeys) {
    const value = query.get(key);
    if (value && /^[a-z0-9_.-]{1,100}$/i.test(value)) pageUrl.searchParams.set(key, value);
  }
  let referrer = '';
  try {
    const url = new URL(document.referrer);
    referrer = `${url.origin}${url.pathname}`;
  } catch { /* Direct visit. */ }

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  const track = (name, parameters = {}) => {
    window.gtag('event', name, { page_path: location.pathname, ...parameters });
  };
  window.ursaAnalytics = { track };
  window.gtag('js', new Date());
  window.gtag('config', measurementId, {
    page_location: pageUrl.href,
    page_referrer: referrer,
    ...(query.get('analytics_debug') === '1' ? { debug_mode: true } : {})
  });

  // Local previews retain an inspectable queue without polluting production GA4.
  if (production) {
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    document.head.append(script);
  }

  const placement = (element) => element.closest('section[id]')?.id
    || (element.closest('.hero') ? 'hero' : element.closest('header') ? 'header' : element.closest('footer') ? 'footer' : 'content');

  document.addEventListener('click', (event) => {
    const link = event.target.closest?.('a[href]');
    if (!link) return;
    const url = new URL(link.href, location.href);
    const parameters = { section_id: placement(link) };
    if (url.protocol === 'mailto:') {
      track('email_click', parameters);
    } else if (url.origin === location.origin && url.hash === '#airtable') {
      track('contact_cta_click', parameters);
    } else if (['http:', 'https:'].includes(url.protocol)) {
      // Only static destination paths; no query strings, contact values, or labels.
      track('resource_click', { ...parameters, link_domain: url.hostname, link_path: url.pathname, link_anchor: url.hash });
    }
  });

  const form = document.getElementById('contact-form');
  form?.addEventListener('input', () => track('contact_form_start', { section_id: 'airtable' }), { once: true });
  document.addEventListener('ursa:contact-draft-open', () => {
    track('contact_email_draft_open', { section_id: 'airtable' });
  });

  // Observe headings, not entire long sections: even tall mobile sections qualify.
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting || entry.intersectionRatio < 0.5 || document.hidden) continue;
        track('section_view', { section_id: placement(entry.target) });
        observer.unobserve(entry.target);
      }
    }, { threshold: 0.5 });
    document.querySelectorAll('main > section[id] h2').forEach((heading) => observer.observe(heading));
  }

  // Measure visible demo playback once per milestone, including autoplay and loops.
  // The decorative hero video is deliberately excluded.
  document.querySelectorAll('video[data-analytics-video]').forEach((video) => {
    let visible = false;
    let started = false;
    let watched = 0;
    let previousTime = video.currentTime;
    const milestones = new Set();
    const details = (percent) => ({
      video_title: video.dataset.analyticsVideo,
      video_provider: 'html5',
      video_percent: percent,
      playback_type: video.autoplay ? 'autoplay' : 'manual'
    });
    const inView = () => {
      if ('IntersectionObserver' in window) return visible;
      const rect = video.getBoundingClientRect();
      return rect.top < window.innerHeight && rect.bottom > 0;
    };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver((entries) => {
        visible = entries[0].isIntersecting && entries[0].intersectionRatio >= 0.5;
        previousTime = video.currentTime;
      }, { threshold: 0.5 }).observe(video);
    }
    video.addEventListener('seeking', () => { previousTime = video.currentTime; });
    video.addEventListener('timeupdate', () => {
      const delta = video.currentTime - previousTime;
      previousTime = video.currentTime;
      if (!inView() || document.hidden || video.paused || video.seeking || !Number.isFinite(video.duration) || video.duration <= 0) return;
      if (!started) {
        started = true;
        track('demo_video_start', details(0));
      }
      // Count actual visible playback, not forward seeks or time spent off screen.
      if (delta > 0 && delta < 2) watched += delta;
      const percent = Math.min(100, Math.round(watched / video.duration * 100));
      for (const milestone of [25, 50, 75, 100]) {
        if (percent >= milestone && !milestones.has(milestone)) {
          milestones.add(milestone);
          track(milestone === 100 ? 'demo_video_complete' : 'demo_video_progress', details(milestone));
        }
      }
    });
  });
})();
