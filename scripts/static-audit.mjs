import fs from 'node:fs';
const html = fs.readFileSync(new URL('../www/index.html', import.meta.url), 'utf8');
const manifest = JSON.parse(fs.readFileSync(new URL('../www/manifest.webmanifest', import.meta.url), 'utf8'));
const pkg = JSON.parse(fs.readFileSync(new URL('../package.json', import.meta.url), 'utf8'));
const mainActivity = fs.readFileSync(new URL('../android/app/src/main/java/app/worldmetrics/mobile/MainActivity.java', import.meta.url), 'utf8');
const checks = [
  ['doctype', html.startsWith('<!DOCTYPE html>')],
  ['manifest linked', html.includes('rel="manifest" href="manifest.webmanifest"')],
  ['no Google Fonts network dependency', !html.includes('fonts.googleapis.com') && !html.includes('fonts.gstatic.com')],
  ['browser save-file control removed', !html.includes('download="world-metrics.html"')],
  ['country data embedded', html.includes('const COUNTRIES = {')],
  ['D3 embedded', html.includes('t.version="7.9.0"') || html.includes('d3.version="7.9.0"')],
  ['TopoJSON embedded', html.includes('topojson-client v3.1.0')],
  ['service worker native guard', html.includes('isNativeCapacitor')],
  ['viewport safe-area support', html.includes('viewport-fit=cover') && html.includes('safe-area-inset-top')],
  ['preferences persistence', html.includes('world-metrics.preferences.v1')],
  ['manifest standalone', manifest.display === 'standalone'],
  ['manifest icons', Array.isArray(manifest.icons) && manifest.icons.length >= 3],
  ['native back bridge', mainActivity.includes('OnBackPressedCallback') && mainActivity.includes('__worldMetricsHandleBack')],
  ['web back priority handler', html.includes('window.__worldMetricsHandleBack') && html.includes('Press back again to exit')],
  ['search selection dismisses keyboard', html.includes('queryEl.blur()')],
  ['pinch zoom uses preview transform', html.includes('setGlobePreviewScale') && html.includes('pinchTargetScale')],
  ['globe redraws coalesced', html.includes('scheduleGlobePaint') && html.includes('globePaintRaf')],
  ['active metric auto-scrolls on mobile', html.includes('ensureMetricVisible') && html.includes('scrollIntoView')],
  ['metric row contained on mobile', html.includes('grid-template-columns: repeat(5, minmax(0, 1fr))')],
  ['orientation toggle', html.includes('orientation-toggle') && mainActivity.includes('WorldMetricsNativeBridge') && mainActivity.includes('SCREEN_ORIENTATION_LANDSCAPE')],
  ['flat map safe geometry fit', html.includes('flatFitObject') && html.includes('projection.fitExtent')],
  ['app version matches package metadata', html.includes(`data-app-version="${pkg.version}"`)]
];
let failed = 0;
for (const [name, pass] of checks) { console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}`); if (!pass) failed++; }
if (failed) process.exit(1);
