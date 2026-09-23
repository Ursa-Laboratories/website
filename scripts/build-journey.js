/* Guide coverage follows Cubware/README.md and documentation/*.md.
   These are documentation routes, not a physical compatibility calculation. */
(() => {
  const root = document.getElementById('build-guides');
  const content = document.getElementById('journey-content');
  if (!root || !content) return;
  const instruments = [
    { id: 'asmi', name: 'ASMI indenter', action: 'Measure material mechanics', description: 'Force-sensor indentation for mechanical characterization.', detail: 'Gantry, sensor mount & plate-holder guides', image: 'assets/asmi_indent.png' },
    { id: 'pipette', name: 'OT-2 pipette', action: 'Move liquids', description: 'Electronic pipetting with a gantry-mounted Opentrons pipette.', detail: 'Build, wiring & commissioning guide' },
    { id: 'capper', name: 'Vial capper / decapper', action: 'Work with vials', description: 'Magnetic cap handling for 20 mL vials on the PANDA deck.', detail: 'Parts, assembly & wiring guide' },
  ];
  const platforms = [
    { id: 'cub', name: 'Cub', label: 'Compact bench setup', base: '3018-PROVer V2', description: 'A starting point for single-instrument characterization.', guide: 'cub-calibration.html', assembly: 'cub-gantry-build.html' },
    { id: 'cubxl', name: 'CubXL', label: 'Larger bench · ASMI', base: 'PROVerXL 4030 V2', description: 'The force-sensor indentation build with the ASMI deck.', guide: 'cubxl-calibration.html', assembly: 'cubxl-gantry-build.html' },
    { id: 'cubxl-plus', name: 'CubXL+', label: 'Larger bench · PANDA', base: 'PROVerXL 4030 V2', description: 'The non-contact deck for pipetting and vial workflows.', guide: 'cubxl-plus-calibration.html', assembly: 'panda-gantry-build.html' },
  ];
  let selected = new Set();
  let platform = '';
  let step = 0;
  const hasPanda = () => selected.has('pipette') || selected.has('capper');
  const suggested = () => selected.has('asmi') && !hasPanda() ? 'cubxl' : hasPanda() && !selected.has('asmi') ? 'cubxl-plus' : '';
  const toolNames = () => instruments.filter(t => selected.has(t.id)).map(t => t.name).join(' + ') || 'Platform assembly & calibration';
  const linkRow = (href, title, copy) => `<li><a href="${href}"><strong>${title}<span aria-hidden="true">↗</span></strong><span>${copy}</span></a></li>`;
  function render(focus = true) {
    root.hidden = false;
    root.querySelectorAll('.journey-steps li').forEach((el, i) => {
      if (i === step) el.setAttribute('aria-current', 'step'); else el.removeAttribute('aria-current');
      el.classList.toggle('is-complete', i < step);
    });
    if (step === 0) {
      content.innerHTML = `<div class="journey-heading"><h2 tabindex="-1">Start with your experiment.</h2><p>Choose one or more instruments to explore the available build paths.</p></div>
        <div class="instrument-options">${instruments.map(t => `<label class="instrument-option ${t.image ? 'instrument-featured' : ''}">
          <input type="checkbox" name="instrument" value="${t.id}" ${selected.has(t.id) ? 'checked' : ''}>
          ${t.image ? `<img src="${t.image}" alt="ASMI force sensor mounted on a CubXL gantry">` : ''}
          <span class="option-copy"><span class="option-action">${t.action}</span><strong>${t.name}</strong><span>${t.description}</span><small>${t.detail}</small></span>
        </label>`).join('')}</div>
        <div class="journey-actions"><button type="button" class="journey-text-btn" data-action="skip">Just show me platform guides</button><button type="button" class="btn btn-primary" data-action="next" ${selected.size ? '' : 'disabled'}>Choose your footprint <span aria-hidden="true">→</span></button></div>`;
    } else if (step === 1) {
      content.innerHTML = `<div class="journey-heading"><h2 tabindex="-1">Make room for your build.</h2><p>${toolNames()}. Choose the platform you want to explore.</p></div>
        <div class="platform-options">${platforms.map(p => `<label class="platform-option"><input type="radio" name="platform" value="${p.id}" ${platform === p.id ? 'checked' : ''}>
          <span class="platform-label">${p.label}</span><strong>${p.name}</strong><span class="platform-base">${p.base}</span><span>${p.description}</span>${suggested() === p.id ? '<small class="route-match">Documented path for your selection</small>' : ''}</label>`).join('')}</div>
        <p class="journey-footnote">CubXL and CubXL+ share a gantry size; their decks serve different workflows. Check the assembled machine dimensions before planning bench space. For a 4040-PRO MAX kit, use the <a href="docs/cubxl-2-gantry-build.html">CubXL 2.0 guide</a>.</p>
        <div class="journey-actions"><button type="button" class="journey-text-btn" data-action="back">← Instruments</button><button type="button" class="btn btn-primary" data-action="result" ${platform ? '' : 'disabled'}>Find my build guides <span aria-hidden="true">→</span></button></div>`;
    } else {
      const p = platforms.find(p => p.id === platform);
      const gap = (selected.has('asmi') && !['cub', 'cubxl'].includes(platform)) || (hasPanda() && platform !== 'cubxl-plus');
      let links = linkRow(`docs/${p.assembly}`, platform === 'cubxl-plus' ? 'Assemble the PANDA gantry (legacy Rev. 0)' : `Assemble the ${p.name} gantry`, 'Match your kit to the manual’s gantry model and supplied parts.');
      links += linkRow(`docs/${p.guide}`, `Mount the ${p.name} calibration block`, 'Platform-specific parts, mounting steps and the original PDF.');
      if (selected.has('asmi')) {
        links += linkRow(platform === 'cub' ? 'docs/cub-vernier-mount.html' : 'docs/cubxl-vernier-mount.html', `Fit the ${platform === 'cub' ? 'Cub' : 'CubXL'} Vernier force-sensor mount`, 'Printed parts, fasteners and sensor installation.');
        if (platform !== 'cub') links += linkRow('docs/cubxl-asmi-wellplate-holder.html', 'Mount the CubXL ASMI wellplate holder', '96-well plate holder and baseplate fastening.');
      }
      if (selected.has('pipette')) links += linkRow('docs/opentrons-pipette-setup.html', 'Build the OT-2 pipette station', 'CubXL+ / PANDA mount, electronics and commissioning notes.');
      if (selected.has('capper')) links += linkRow('docs/vial-capper-decapper-build.html', 'Build the vial capper / decapper', 'CubXL+ / PANDA magnetic caps, holder, wiring and firmware.');
      content.innerHTML = `<div class="journey-result"><div class="result-overview"><p class="result-kicker">${gap ? 'Your build to explore' : 'Your build path'}</p><h2 tabindex="-1">${p.name}</h2><p>${toolNames()}</p><span class="platform-base">${p.base}</span><button type="button" class="journey-text-btn" data-action="back">Change footprint</button><button type="button" class="journey-text-btn" data-action="restart">Edit instruments</button></div>
        <div class="result-guides"><h3>${gap ? 'Start with the available guides.' : 'Here’s where to start.'}</h3>
        ${gap ? `<p class="journey-notice">This exact combination does not have a complete build guide. The force-sensor guide below is specific to its named platform; pipette and capper guides describe CubXL+ / PANDA. Your ${p.name} calibration guide is included separately.</p>` : '<p>Follow the platform reference, then explore your instrument guides.</p>'}
        <ol class="result-guide-list">${links}</ol><p class="journey-footnote">These guides cover individual assemblies. Instrument commissioning and a complete system build may require additional steps.</p>
        ${gap ? '<a class="build-card-cta" href="index.html#airtable">Talk through this configuration with us →</a>' : ''}</div></div>
        <div class="journey-actions"><a class="journey-text-btn" href="#guide-library">Browse every guide</a><button type="button" class="journey-text-btn" data-action="reset">Start over ↻</button></div>`;
    }
    if (focus) content.querySelector('h2').focus({ preventScroll: true });
  }
  content.addEventListener('change', e => {
    if (e.target.name === 'instrument') {
      if (e.target.checked) selected.add(e.target.value); else selected.delete(e.target.value);
      content.querySelector('[data-action="next"]').disabled = selected.size === 0;
    }
    if (e.target.name === 'platform') {
      platform = e.target.value;
      content.querySelector('[data-action="result"]').disabled = false;
    }
  });
  content.addEventListener('click', e => {
    const action = e.target.closest('[data-action]')?.dataset.action;
    if (!action) return;
    if (action === 'next' && selected.size) step = 1;
    else if (action === 'skip') { selected.clear(); step = 1; }
    else if (action === 'result' && platform) step = 2;
    else if (action === 'back') step--;
    else if (action === 'restart') step = 0;
    else if (action === 'reset') { step = 0; selected.clear(); platform = ''; }
    else return;
    render();
    root.scrollIntoView({ behavior: 'instant', block: 'start' });
  });
  render(false);
})();
