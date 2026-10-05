from __future__ import annotations

from pathlib import Path
from urllib.request import urlopen
import hashlib
import json
import math
import struct
import zlib

ROOT = Path.cwd()
UPSTREAM_REPO = "refat247/world-metrics"
UPSTREAM_COMMIT = "9bad10f022e2d07ffdf036d33ddf1b0e37fbe7ed"
EXPECTED_GIT_BLOB = "79487b79286ce7c8dbae0685db33ddaefffdeaee"
SOURCE_URL = f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/{UPSTREAM_COMMIT}/public/world-metrics.html"
VERSION = "1.0.0"


def write_text(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def write_bytes(path: str, body: bytes) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(body)


def git_blob_sha(body: bytes) -> str:
    header = f"blob {len(body)}\0".encode("utf-8")
    return hashlib.sha1(header + body).hexdigest()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def png_rgba(size: int, maskable: bool = False) -> bytes:
    bg = (13, 17, 23, 255)
    accent = (63, 208, 201, 255)
    dim = (31, 110, 105, 255)
    rows = []
    cx = cy = (size - 1) / 2
    radius = size * (0.29 if maskable else 0.36)
    line = max(1.0, size / 80)
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            dx, dy = x - cx, y - cy
            r = math.hypot(dx, dy)
            pix = bg
            if abs(r - radius) <= line * 1.6:
                pix = accent
            elif r < radius:
                lon = abs(math.sin((dx / max(radius, 1)) * math.pi * 2))
                lat = abs(math.sin((dy / max(radius, 1)) * math.pi * 2))
                if lon > 0.88 or lat > 0.91:
                    pix = dim
            row.extend(pix)
        rows.append(bytes(row))
    raw = b"".join(rows)
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")


def build_html(source: str) -> str:
    text = source
    text = replace_once(
        text,
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="theme-color" content="#0d1117">\n'
        '<meta name="color-scheme" content="dark">\n'
        '<meta name="mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
        '<meta name="apple-mobile-web-app-title" content="World Metrics">\n'
        '<link rel="manifest" href="manifest.webmanifest">\n'
        '<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">\n'
        '<link rel="apple-touch-icon" href="icons/icon-192.png">',
        "PWA head",
    )
    text = replace_once(
        text,
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">\n',
        '',
        "external Google Fonts",
    )
    text = replace_once(
        text,
        'html, body { height: 100%; margin: 0; background: var(--color-bg); color: var(--color-fg); }',
        'html, body { height: 100%; margin: 0; background: var(--color-bg); color: var(--color-fg); overscroll-behavior: none; }\n'
        '* { box-sizing: border-box; }\n'
        'body { -webkit-tap-highlight-color: transparent; }',
        "mobile CSS",
    )
    text = replace_once(
        text,
        '  overflow: hidden;\n  font-family: var(--font-sans);\n}',
        '  overflow: hidden;\n  font-family: var(--font-sans);\n'
        '  padding-top: env(safe-area-inset-top);\n'
        '  padding-right: env(safe-area-inset-right);\n'
        '  padding-bottom: env(safe-area-inset-bottom);\n'
        '  padding-left: env(safe-area-inset-left);\n}',
        "safe area CSS",
    )
    text = replace_once(text, '<div class="app" id="app">', '<div class="app" id="app" data-app-version="1.0.0">', "app version")
    text = replace_once(text, '    <a class="save-file" href="world-metrics.html" download="world-metrics.html">Save file</a>\n', '', "save-file control")
    text = replace_once(
        text,
        '  let metric = "gdp_per_capita";\n  let mode = "flat";',
        '  const PREF_KEY = "world-metrics.preferences.v1";\n'
        '  function readPreferences() {\n'
        '    try { return JSON.parse(localStorage.getItem(PREF_KEY) || "{}"); } catch (_) { return {}; }\n'
        '  }\n'
        '  function savePreference(key, value) {\n'
        '    try {\n'
        '      const prefs = readPreferences();\n'
        '      prefs[key] = value;\n'
        '      localStorage.setItem(PREF_KEY, JSON.stringify(prefs));\n'
        '    } catch (_) {}\n'
        '  }\n'
        '  const initialPrefs = readPreferences();\n'
        '  let metric = METRIC_KEYS.includes(initialPrefs.metric) ? initialPrefs.metric : "gdp_per_capita";\n'
        '  let mode = "flat";',
        "preferences",
    )
    text = replace_once(text, '    mode = next;\n    svg.classList.toggle("globe", next === "globe");', '    mode = next;\n    savePreference("mode", next);\n    svg.classList.toggle("globe", next === "globe");', "mode persistence")
    text = replace_once(text, '      metric = key;\n      renderLegend();', '      metric = key;\n      savePreference("metric", key);\n      renderLegend();', "metric persistence")
    text = replace_once(
        text,
        '  renderLegend();\n  status.remove();\n  raf = requestAnimationFrame(spin);\n})();',
        '  renderLegend();\n  status.remove();\n  if (initialPrefs.mode === "globe") setMode("globe");\n  raf = requestAnimationFrame(spin);\n\n'
        '  // PWA caching is browser-only. Avoid registering a service worker inside\n'
        "  // Capacitor's native WebView because it can interfere with native bridge injection.\n"
        '  const isNativeCapacitor = Boolean(window.Capacitor && window.Capacitor.isNativePlatform && window.Capacitor.isNativePlatform());\n'
        '  if ("serviceWorker" in navigator && !isNativeCapacitor && (location.protocol === "https:" || location.hostname === "localhost" || location.hostname === "127.0.0.1")) {\n'
        '    window.addEventListener("load", () => navigator.serviceWorker.register("service-worker.js").catch(() => {}));\n'
        '  }\n})();',
        "PWA registration",
    )
    return text


raw = urlopen(SOURCE_URL, timeout=60).read()
actual = git_blob_sha(raw)
if actual != EXPECTED_GIT_BLOB:
    raise RuntimeError(f"upstream provenance mismatch: expected {EXPECTED_GIT_BLOB}, got {actual}")

write_bytes("artifacts/original/world-metrics.html", raw)
product_html = build_html(raw.decode("utf-8"))
write_text("www/index.html", product_html)

manifest = {
    "name": "World Metrics",
    "short_name": "World Metrics",
    "description": "Interactive offline-first world metrics explorer.",
    "id": "/",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "any",
    "background_color": "#0d1117",
    "theme_color": "#0d1117",
    "categories": ["education", "reference", "utilities"],
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
write_text("www/manifest.webmanifest", json.dumps(manifest, indent=2) + "\n")

write_text("www/service-worker.js", '''const CACHE = "world-metrics-v1.0.0";
const CORE = ["./", "./index.html", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/icon-maskable-512.png"];
self.addEventListener("install", (event) => { event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener("activate", (event) => { event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(caches.match(event.request).then((cached) => cached || fetch(event.request).then((response) => {
    const copy = response.clone(); caches.open(CACHE).then((cache) => cache.put(event.request, copy)); return response;
  }).catch(() => caches.match("./index.html"))));
});
''')

for path, size, maskable in [
    ("www/icons/icon-192.png", 192, False),
    ("www/icons/icon-512.png", 512, False),
    ("www/icons/icon-maskable-512.png", 512, True),
    ("assets/icon.png", 1024, False),
    ("assets/icon-maskable.png", 1024, True),
]:
    write_bytes(path, png_rgba(size, maskable))
write_text("assets/icon.svg", '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="96" fill="#0d1117"/><circle cx="256" cy="256" r="158" fill="none" stroke="#3fd0c9" stroke-width="18"/><path d="M98 256h316M256 98c58 54 88 106 88 158s-30 104-88 158M256 98c-58 54-88 106-88 158s30 104 88 158" fill="none" stroke="#1f6e69" stroke-width="14"/></svg>\n''')

write_text("package.json", '''{
  "name": "world-metrics-app",
  "version": "1.0.0",
  "private": true,
  "description": "Offline-first World Metrics PWA and Capacitor Android/iOS app",
  "scripts": {
    "serve": "python -m http.server 4173 --directory www",
    "cap:add:android": "npx cap add android",
    "cap:add:ios": "npx cap add ios",
    "cap:sync": "npx cap sync",
    "cap:open:android": "npx cap open android",
    "cap:open:ios": "npx cap open ios",
    "android:debug": "cd android && ./gradlew assembleDebug",
    "android:bundle": "cd android && ./gradlew bundleRelease",
    "audit:static": "node scripts/static-audit.mjs",
    "audit:lineage": "node scripts/verify-lineage.mjs",
    "audit": "npm run audit:static && npm run audit:lineage"
  },
  "dependencies": {
    "@capacitor/android": "8.5.2",
    "@capacitor/core": "8.5.2",
    "@capacitor/ios": "8.5.2"
  },
  "devDependencies": { "@capacitor/cli": "8.5.2" }
}
''')
write_text("capacitor.config.json", '''{
  "appId": "app.worldmetrics.mobile",
  "appName": "World Metrics",
  "webDir": "www",
  "backgroundColor": "#0d1117",
  "android": { "allowMixedContent": false, "backgroundColor": "#0d1117" }
}
''')
write_text(".gitignore", '''node_modules/
.DS_Store
*.log
android/.gradle/
android/app/build/
android/build/
*.jks
*.keystore
android/
ios/
''')

write_text("scripts/verify-lineage.mjs", '''import fs from 'node:fs';
import crypto from 'node:crypto';
const EXPECTED = '79487b79286ce7c8dbae0685db33ddaefffdeaee';
const path = new URL('../artifacts/original/world-metrics.html', import.meta.url);
const body = fs.readFileSync(path);
const header = Buffer.from(`blob ${body.length}\\0`, 'utf8');
const actual = crypto.createHash('sha1').update(header).update(body).digest('hex');
console.log(`Expected Grok canonical HTML blob: ${EXPECTED}`);
console.log(`Production provenance HTML blob:     ${actual}`);
if (actual !== EXPECTED) process.exit(1);
console.log('PASS  provenance HTML is byte-identical to the Grok canonical source');
''')
write_text("scripts/static-audit.mjs", '''import fs from 'node:fs';
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
''')

write_text("SETUP_ANDROID_WINDOWS.bat", '''@echo off
setlocal
where node >nul 2>nul || (echo Node.js 22+ is required.& exit /b 1)
call npm install || exit /b 1
if not exist android call npx cap add android || exit /b 1
call npx cap sync android || exit /b 1
call npx cap open android
''')
write_text("SYNC_ANDROID_WINDOWS.bat", '''@echo off
setlocal
call npx cap sync android || exit /b 1
call npx cap open android
''')
write_text("SETUP_IOS_MAC.command", '''#!/bin/sh
set -eu
npm install
[ -d ios ] || npx cap add ios
npx cap sync ios
npx cap open ios
''')

write_text("README.md", f'''# World Metrics App

**Role:** PRODUCT CANONICAL  
**Version:** {VERSION}

Production PWA + Capacitor Android/iOS lineage derived from the preserved Grok reference implementation.

## Repository authority

- Grok reference canonical: `refat247/world-metrics`
- Frozen Grok baseline: `archive/grok-canonical-v1.0`
- Baseline commit: `{UPSTREAM_COMMIT}`
- Canonical HTML Git blob: `{EXPECTED_GIT_BLOB}`
- Active production canonical: this repository, `refat247/world-metrics-app`

`artifacts/original/world-metrics.html` is fetched only from that pinned commit during bootstrap and is accepted only if its Git blob SHA matches the expected canonical value.

## Audit

```bash
npm run audit
```

## Browser / PWA

```bash
python -m http.server 4173 --directory www
```

Open `http://localhost:4173`.

## Android

On Windows, double-click `SETUP_ANDROID_WINDOWS.bat` after installing Node.js 22+ and Android Studio. The script installs the pinned Capacitor dependencies, creates the native Android project, syncs the web assets, and opens Android Studio.

## iOS

Requires macOS + Xcode. Run `SETUP_IOS_MAC.command`.

## Design rule

Do not merge Grok/App-Builder infrastructure into this repository merely because it exists upstream. Product features belong here; the Grok repository remains the preserved comparison/reference lineage.
''')
write_text("REPOSITORY_ROLE.md", f'''# Repository Role — PRODUCT CANONICAL

This repository is the authoritative production lineage for World Metrics.

The Grok-generated repository `refat247/world-metrics` remains preserved as a separate reference lineage. Its frozen baseline is `archive/grok-canonical-v1.0` at `{UPSTREAM_COMMIT}`.

The source HTML used to derive this product must verify to Git blob `{EXPECTED_GIT_BLOB}` before generation.
''')
write_text("docs/LINEAGE.md", f'''# World Metrics Lineage

## Source artifact

The original self-contained World Metrics HTML is preserved in the Grok reference repository.

## Grok canonical/reference

- Repository: `refat247/world-metrics`
- Frozen branch: `archive/grok-canonical-v1.0`
- Commit: `{UPSTREAM_COMMIT}`
- Canonical HTML path: `public/world-metrics.html`
- Canonical HTML Git blob: `{EXPECTED_GIT_BLOB}`

## Product canonical

- Repository: `refat247/world-metrics-app`
- Role: active PWA + Capacitor Android/iOS product development
- Provenance copy: `artifacts/original/world-metrics.html`

`scripts/verify-lineage.mjs` proves the provenance copy is byte-identical to the Grok canonical HTML by recomputing Git's blob SHA.
''')
write_text("docs/ANDROID_BUILD_GUIDE.md", '''# Android Build Guide

1. Install Node.js 22+ and Android Studio with a current Android SDK.
2. Clone this repository.
3. Run `SETUP_ANDROID_WINDOWS.bat`.
4. Let Android Studio finish Gradle sync.
5. Run on a connected Android device or emulator.
6. For a Play Store release, configure signing and build an Android App Bundle (`.aab`).

The generated `android/` directory is intentionally ignored at v1.0.0 and may be regenerated from the canonical web assets and Capacitor config.
''')
write_text("docs/IOS_BUILD_GUIDE.md", '''# iOS Build Guide

1. Use macOS with Xcode installed.
2. Install Node.js 22+.
3. Clone this repository and run `SETUP_IOS_MAC.command`.
4. Configure the Apple team, bundle signing, icons/splash assets, privacy metadata, and App Store listing in Xcode/App Store Connect.

The generated `ios/` directory is intentionally ignored at v1.0.0 and may be regenerated from the canonical web assets and Capacitor config.
''')
write_text("docs/RELEASE_AUDIT.md", f'''# Release Audit — World Metrics App v{VERSION}

## Provenance

- Grok baseline commit: `{UPSTREAM_COMMIT}`
- Expected source HTML Git blob: `{EXPECTED_GIT_BLOB}`
- Bootstrap refuses to continue if the downloaded pinned source does not match that blob.

## Product checks

`npm run audit` validates 12 static/PWA invariants plus the byte-level lineage invariant.

## Native build boundary

Capacitor source/configuration is canonical here. Android and iOS native projects are generated on development machines because Android SDK/Xcode toolchains are not committed in this v1.0.0 lineage.
''')
write_text("docs/GITHUB_BOOTSTRAP.md", '''# GitHub Bootstrap

The repository was initialized from an empty GitHub repository by a one-use workflow. The workflow downloaded the source only from the pinned Grok commit, verified its Git blob SHA, generated the PWA/Capacitor product tree, ran integrity audits, committed the materialized result, and then removed the one-use bootstrap workflow.

The deterministic bootstrap script remains at `scripts/bootstrap_from_grok.py` for provenance and reproducibility.
''')

write_text(".github/workflows/ci.yml", '''name: Production integrity
on:
  push:
    branches: ['**']
  pull_request:
permissions:
  contents: read
jobs:
  integrity:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: npm run audit
''')

bootstrap_workflow = ROOT / ".github/workflows/bootstrap-product-canonical.yml"
if bootstrap_workflow.exists():
    bootstrap_workflow.unlink()

# Deterministic release hashes for canonical non-generated/native-independent files.
paths = sorted(p for p in ROOT.rglob('*') if p.is_file() and '.git/' not in p.as_posix() and p.name != 'SHA256SUMS.txt')
lines = []
for p in paths:
    rel = p.relative_to(ROOT).as_posix()
    lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {rel}")
write_text("docs/SHA256SUMS.txt", "\n".join(lines) + "\n")

print(f"PASS upstream Git blob {actual}")
print("PASS materialized World Metrics PRODUCT-CANONICAL v1.0.0")
