import fs from 'node:fs';
const html = fs.readFileSync(new URL('../www/index.html', import.meta.url), 'utf8');
const manifest = JSON.parse(fs.readFileSync(new URL('../www/manifest.webmanifest', import.meta.url), 'utf8'));
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
  ['manifest icons', Array.isArray(manifest.icons) && manifest.icons.length >= 3]
];
let failed = 0;
for (const [name, pass] of checks) { console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}`); if (!pass) failed++; }
if (failed) process.exit(1);
