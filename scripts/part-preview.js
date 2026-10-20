import * as THREE from 'three';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

export function createPreview(canvas, report) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor('#edf1f6');
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 10000);
  const controls = new OrbitControls(camera, canvas);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x718099, 2.5));
  const light = new THREE.DirectionalLight(0xffffff, 3);
  light.position.set(2, 5, 3);
  scene.add(light);
  const fill = new THREE.DirectionalLight(0xc7dcff, 1.2);
  fill.position.set(-3, 1, -2);
  scene.add(fill);
  let model = null;
  let radius = 1;
  let generation = 0;
  let request;
  let wireframe = false;
  let view = 'iso';
  let contextLost = false;
  const directions = {
    iso: new THREE.Vector3(1, .8, 1),
    top: new THREE.Vector3(0, 1, .00001),
    front: new THREE.Vector3(0, 0, 1),
    side: new THREE.Vector3(1, 0, 0),
  };
  const render = () => { if (!contextLost) renderer.render(scene, camera); };
  controls.addEventListener('change', render);

  function dispose(object) {
    object.traverse(child => {
      child.geometry?.dispose();
      const materials = Array.isArray(child.material) ? child.material : [child.material];
      for (const material of materials.filter(Boolean)) {
        for (const value of Object.values(material)) if (value?.isTexture) value.dispose();
        material.dispose();
      }
    });
  }

  function clear() {
    ++generation;
    request?.abort();
    delete canvas.dataset.loadedPart;
    if (model) { scene.remove(model); dispose(model); model = null; }
    render();
  }

  function setView(name = 'iso') {
    view = name;
    const halfFov = THREE.MathUtils.degToRad(camera.fov / 2);
    const limitingFov = Math.min(halfFov, Math.atan(Math.tan(halfFov) * camera.aspect));
    const distance = radius / Math.sin(limitingFov) * 1.22;
    camera.position.copy(directions[name] || directions.iso).normalize().multiplyScalar(distance);
    camera.near = Math.max(radius / 1000, .00001);
    camera.far = radius * 1000;
    camera.updateProjectionMatrix();
    controls.minDistance = radius * .15;
    controls.maxDistance = radius * 30;
    controls.target.set(0, 0, 0);
    controls.update();
    render();
  }

  new ResizeObserver(() => {
    const { width, height } = canvas.parentElement.getBoundingClientRect();
    renderer.setSize(width, height, false);
    camera.aspect = width / Math.max(height, 1);
    camera.updateProjectionMatrix();
    if (model) setView(view); else render();
  }).observe(canvas.parentElement);

  canvas.addEventListener('webglcontextlost', event => {
    event.preventDefault();
    contextLost = true;
    clear();
    report('The 3D graphics context was lost. Reload the page to restore it; source downloads are still available.');
  });
  canvas.addEventListener('keydown', event => {
    if (!model) return;
    const offset = camera.position.clone().sub(controls.target);
    const spherical = new THREE.Spherical().setFromVector3(offset);
    const actions = {
      ArrowLeft: () => { spherical.theta -= .12; },
      ArrowRight: () => { spherical.theta += .12; },
      ArrowUp: () => { spherical.phi -= .12; },
      ArrowDown: () => { spherical.phi += .12; },
      '+': () => { spherical.radius *= .9; },
      '=': () => { spherical.radius *= .9; },
      '-': () => { spherical.radius *= 1.1; },
    };
    if (!actions[event.key]) return;
    event.preventDefault();
    actions[event.key]();
    spherical.makeSafe();
    spherical.radius = THREE.MathUtils.clamp(spherical.radius, controls.minDistance, controls.maxDistance);
    camera.position.setFromSpherical(spherical).add(controls.target);
    controls.update();
    render();
  });

  return {
    clear,
    setView,
    setWireframe(enabled) {
      wireframe = enabled;
      model?.traverse(child => {
        for (const material of [child.material].flat().filter(Boolean)) material.wireframe = enabled;
      });
      render();
    },
    async load(part) {
      clear();
      if (contextLost) throw new Error('Graphics context lost');
      const version = generation;
      request = new AbortController();
      const response = await fetch(part.file, { signal: request.signal });
      if (!response.ok) throw new Error(`Mesh request failed (${response.status})`);
      const buffer = await response.arrayBuffer();
      if (version !== generation) return null;
      let object;
      if (part.file.toLowerCase().endsWith('.glb')) {
        object = (await new GLTFLoader().parseAsync(buffer, '')).scene;
      } else {
        const geometry = new STLLoader().parse(buffer);
        geometry.computeVertexNormals();
        object = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({
          color: 0x6c8eb3, metalness: .12, roughness: .47, side: THREE.DoubleSide,
        }));
        object.rotation.x = -Math.PI / 2;
      }
      if (version !== generation) { dispose(object); return null; }
      const box = new THREE.Box3().setFromObject(object);
      const size = box.getSize(new THREE.Vector3());
      if (![size.x, size.y, size.z].every(Number.isFinite) || !size.length()) {
        dispose(object);
        throw new Error('No usable geometry in this file');
      }
      object.position.sub(box.getCenter(new THREE.Vector3()));
      radius = size.length() / 2;
      model = object;
      scene.add(model);
      this.setWireframe(wireframe);
      setView('iso');
      canvas.dataset.loadedPart = part.id;
      // STL previews are Z-up in the source. GLB follows glTF's Y-up convention.
      return part.file.endsWith('.glb') ? [size.x, size.y, size.z] : [size.x, size.z, size.y];
    },
  };
}
