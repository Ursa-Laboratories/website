import * as THREE from 'three';
      import { STLLoader } from 'three/addons/loaders/STLLoader.js';
      import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

      try {
      const response = await fetch('assets/cad/catalog.json');
      if (!response.ok) throw new Error('Could not fetch CAD catalog');
      const catalogData = await response.json();
      const catalog = Array.isArray(catalogData) ? catalogData : catalogData.parts;
      const PARTS = Object.fromEntries(catalog.map(part => [part.id, part]));
      const catalogEl = document.getElementById('cad-catalog');
      const searchEl = document.getElementById('cad-search');
      const countEl = document.getElementById('cad-count');
      const titleEl = document.getElementById('cad-part-title');
      const sourceEl = document.getElementById('cad-part-source');
      const downloadEl = document.getElementById('cad-download');
      const categoryOrder = ['Cub', 'CubXL', 'CubXL+', 'Labware'];
      let currentId = '';
      for (const group of categoryOrder) {
        const parts = catalog.filter(part => part.group === group);
        const category = document.createElement('details');
        category.className = 'cad-category';
        category.dataset.group = group;
        const summary = document.createElement('summary');
        summary.textContent = `${group} (${parts.length})`;
        category.append(summary);
        const folders = [...new Set(parts.map(part => part.subgroup || 'Parts'))];
        for (const folder of folders) {
          const section = document.createElement('details');
          section.className = 'cad-folder';
          const heading = document.createElement('summary');
          heading.textContent = folder;
          section.append(heading);
          const list = document.createElement('div');
          list.className = 'cad-part-buttons';
          list.setAttribute('role', 'group');
          list.setAttribute('aria-label', `${group}: ${folder}`);
          for (const part of parts.filter(part => (part.subgroup || 'Parts') === folder)) {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'cad-part-btn';
            button.dataset.part = part.id;
            button.dataset.search = `${part.label} ${part.subgroup} ${part.source || ''}`.toLowerCase();
            button.textContent = part.label;
            button.setAttribute('aria-pressed', 'false');
            list.append(button);
          }
          section.append(list);
          category.append(section);
        }
        catalogEl.append(category);
      }
      countEl.textContent = `${catalog.length} parts and assemblies`;
      searchEl.addEventListener('input', () => {
        const query = searchEl.value.trim().toLowerCase();
        let shown = 0;
        catalogEl.querySelectorAll('.cad-part-btn').forEach(button => {
          button.hidden = !button.dataset.search.includes(query);
          if (!button.hidden) shown++;
        });
        catalogEl.querySelectorAll('.cad-folder').forEach(folder => {
          folder.hidden = !folder.querySelector('.cad-part-btn:not([hidden])');
          folder.open = Boolean(query) || Boolean(folder.querySelector(`[data-part="${currentId}"]`));
        });
        catalogEl.querySelectorAll('.cad-category').forEach(category => {
          category.hidden = !category.querySelector('.cad-part-btn:not([hidden])');
          category.open = Boolean(query) || Boolean(category.querySelector(`[data-part="${currentId}"]`));
        });
        countEl.textContent = query ? `${shown} of ${catalog.length} parts match` : `${catalog.length} parts and assemblies`;
      });

      const canvas = document.getElementById('cad-canvas');
      const status = document.getElementById('cad-status');
      const descEl = document.getElementById('cad-part-desc');
      const buttons = document.querySelectorAll('.cad-part-btn');
      const wrap = canvas.parentElement;

      const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 5000);
      scene.add(new THREE.HemisphereLight(0xffffff, 0x44506b, 1.1));
      const keyLight = new THREE.DirectionalLight(0xffffff, 1.4);
      keyLight.position.set(1, 2, 1.5);
      scene.add(keyLight);
      const fillLight = new THREE.DirectionalLight(0xbcd3ff, 0.5);
      fillLight.position.set(-1.5, -0.5, -1);
      scene.add(fillLight);

      const controls = new OrbitControls(camera, canvas);
      controls.enableDamping = true;
      controls.autoRotate = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      controls.autoRotateSpeed = 1.6;

      const material = new THREE.MeshStandardMaterial({ color: 0x3f6fd1, metalness: 0.1, roughness: 0.55 });
      const loader = new STLLoader();
      let mesh = null;
      let loadVersion = 0;

      function resize() {
        const w = wrap.clientWidth;
        const h = wrap.clientHeight;
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
      }
      new ResizeObserver(resize).observe(wrap);
      resize();

      function frameObject(geometry) {
        geometry.computeBoundingBox();
        const box = geometry.boundingBox;
        const center = new THREE.Vector3();
        box.getCenter(center);
        geometry.translate(-center.x, -center.y, -center.z);
        // STLs are Z-up; three.js is Y-up
        geometry.rotateX(-Math.PI / 2);
        geometry.computeBoundingBox();
        const size = new THREE.Vector3();
        geometry.boundingBox.getSize(size);
        const radius = size.length() / 2;
        camera.position.set(radius * 2.2, radius * 1.4, radius * 2.2);
        camera.near = radius / 100;
        camera.far = radius * 100;
        camera.updateProjectionMatrix();
        controls.target.set(0, 0, 0);
        controls.update();
      }

      function loadPart(id) {
        const part = PARTS[id];
        if (!part) return;
        const version = ++loadVersion;
        currentId = id;
        titleEl.textContent = part.label;
        sourceEl.textContent = part.source || (part.sources || []).join(' · ');
        downloadEl.href = part.file;
        downloadEl.hidden = !part.file;
        canvas.setAttribute('aria-label', `3D preview: ${part.label}`);
        buttons.forEach((b) => {
          const active = b.dataset.part === id;
          b.classList.toggle('active', active);
          b.setAttribute('aria-pressed', String(active));
        });
        descEl.textContent = part.desc || part.status || '';
        if (!part.file) { status.hidden = false; status.textContent = 'Preview unavailable for this source file.'; return; }
        delete canvas.dataset.loadedPart;
        status.textContent = 'Loading model…';
        status.hidden = false;
        loader.load(
          part.file,
          (geometry) => {
            if (version !== loadVersion) { geometry.dispose(); return; }
            if (mesh) {
              scene.remove(mesh);
              mesh.geometry.dispose();
            }
            frameObject(geometry);
            mesh = new THREE.Mesh(geometry, material);
            scene.add(mesh);
            canvas.dataset.loadedPart = id;
            status.hidden = true;
          },
          undefined,
          () => {
            if (version !== loadVersion) return;
            status.textContent = 'Could not load this model.';
          }
        );
      }

      buttons.forEach((btn) => btn.addEventListener('click', () => loadPart(btn.dataset.part)));
      const first = catalog.find(part => (part.source || '').endsWith('ForceSensorMountFront.stl')) || catalog[0];
      if (first) {
        loadPart(first.id);
        const selected = catalogEl.querySelector(`[data-part="${first.id}"]`);
        selected.closest('.cad-folder').open = true;
        selected.closest('.cad-category').open = true;
      }

      renderer.setAnimationLoop(() => {
        controls.update();
        renderer.render(scene, camera);
      });

      } catch (error) {
        document.getElementById('cad-status').textContent = 'Could not load the CAD catalog. Please refresh or browse the CAD files.';
        document.getElementById('cad-status').hidden = false;
        document.getElementById('cad-count').textContent = 'Catalog unavailable';
      }
