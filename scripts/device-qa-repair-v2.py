from pathlib import Path
import json, re, shutil
ROOT=Path(__file__).resolve().parents[1]
html_path=ROOT/'www/index.html'
html=html_path.read_text(encoding='utf-8')

def once(old,new,label):
    global html
    if new in html:
        return
    if old not in html:
        raise SystemExit(f'missing marker: {label}')
    html=html.replace(old,new,1)

html=html.replace('data-app-version="1.0.1"','data-app-version="1.0.2"',1)

once('''  .metric-switcher {\n    scroll-snap-type: x proximity;\n  }''','''  .metric-switcher {\n    width: 100%;\n    min-width: 0;\n    flex: 1 1 100%;\n    display: grid;\n    grid-template-columns: repeat(5, minmax(0, 1fr));\n    overflow: hidden;\n    scroll-snap-type: none;\n  }''','mobile metric grid')
once('''  .metric-btn {\n    flex: 0 0 auto;\n    scroll-snap-align: center;\n  }''','''  .metric-btn {\n    width: 100%;\n    min-width: 0;\n    justify-content: center;\n    padding-left: 3px;\n    padding-right: 3px;\n    font-size: clamp(9px, 2.55vw, 11px);\n    letter-spacing: 0;\n    overflow: hidden;\n    text-overflow: clip;\n    scroll-snap-align: none;\n  }\n\n  .orientation-btn {\n    min-height: 44px;\n  }''','mobile metric buttons')

once('''.mode-btn[aria-checked="true"] {\n  color: var(--color-bg);\n  background: var(--color-amber);\n  font-weight: 600;\n}\n''','''.mode-btn[aria-checked="true"] {\n  color: var(--color-bg);\n  background: var(--color-amber);\n  font-weight: 600;\n}\n\n.orientation-btn {\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  gap: 6px;\n  min-height: 36px;\n  padding: 8px 10px;\n  border: 1px solid var(--color-line);\n  border-radius: 8px;\n  background: var(--color-surface-2);\n  color: var(--color-muted);\n  font-family: var(--font-mono);\n  font-size: 11px;\n  white-space: nowrap;\n}\n\n.orientation-btn:hover {\n  color: var(--color-fg);\n  background: #1b2530;\n}\n''','orientation styles')

once('''    <div class="switcher" role="radiogroup" aria-label="Map mode">\n      <button type="button" class="mode-btn" data-mode="flat" role="radio" aria-checked="true">Flat</button>\n      <button type="button" class="mode-btn" data-mode="globe" role="radio" aria-checked="false" title="Drag to rotate. The globe turns slowly until you grab it.">Globe</button>\n    </div>''','''    <div class="switcher" role="radiogroup" aria-label="Map mode">\n      <button type="button" class="mode-btn" data-mode="flat" role="radio" aria-checked="true">Flat</button>\n      <button type="button" class="mode-btn" data-mode="globe" role="radio" aria-checked="false" title="Drag to rotate. The globe turns slowly until you grab it.">Globe</button>\n    </div>\n    <button type="button" class="orientation-btn" id="orientation-toggle" aria-label="Switch to landscape orientation" title="Switch portrait / landscape">\n      <span aria-hidden="true">↻</span><span id="orientation-label">Landscape</span>\n    </button>''','orientation button html')

once('''  const resultsEl = document.getElementById("results");\n  const queryEl = document.getElementById("query");''','''  const resultsEl = document.getElementById("results");\n  const queryEl = document.getElementById("query");\n  const orientationBtn = document.getElementById("orientation-toggle");\n  const orientationLabel = document.getElementById("orientation-label");''','orientation refs')

old='''  function fitFlat() {\n    projection.fitExtent(\n      [\n        [8, 8],\n        [Math.max(16, width - 8), Math.max(16, height - 8)],\n      ],\n      { type: "Sphere" },\n    );\n    if (isMobile() && height > width) {\n      projection.scale(projection.scale() * 1.12).translate([width / 2, height * 0.44]);\n    }\n    zoomBehavior.extent([\n      [0, 0],\n      [width, height],\n    ]).translateExtent([\n      [0, 0],\n      [width, height],\n    ]);\n    redrawFlat();\n  }'''
new='''  const flatFitObject = { type: "FeatureCollection", features: features };\n  function fitFlat() {\n    const inset = isMobile() ? 6 : 8;\n    projection.fitExtent(\n      [\n        [inset, inset],\n        [Math.max(inset + 1, width - inset), Math.max(inset + 1, height - inset)],\n      ],\n      flatFitObject,\n    );\n    if (isMobile() && height > width) {\n      const bounds = flatPath.bounds(flatFitObject);\n      const currentCenterY = (bounds[0][1] + bounds[1][1]) / 2;\n      const mapHeight = Math.max(1, bounds[1][1] - bounds[0][1]);\n      const safeTop = 12;\n      const safeBottom = height - 12;\n      const desiredCenterY = Math.min(\n        safeBottom - mapHeight / 2,\n        Math.max(safeTop + mapHeight / 2, height * 0.43),\n      );\n      const translate = projection.translate();\n      projection.translate([translate[0], translate[1] + desiredCenterY - currentCenterY]);\n    }\n    zoomBehavior.extent([\n      [0, 0],\n      [width, height],\n    ]).translateExtent([\n      [0, 0],\n      [width, height],\n    ]);\n    redrawFlat();\n  }'''
once(old,new,'flat safe fit')

marker='''  function ensureMetricVisible(button) {\n    if (!button || !isMobile()) return;\n    button.scrollIntoView({ behavior: reducedMotion() ? "auto" : "smooth", block: "nearest", inline: "center" });\n  }'''
replacement=marker+'''\n  function currentOrientation() {\n    return window.innerWidth > window.innerHeight ? "landscape" : "portrait";\n  }\n  function updateOrientationControl() {\n    if (!orientationBtn || !orientationLabel) return;\n    const target = currentOrientation() === "portrait" ? "landscape" : "portrait";\n    orientationLabel.textContent = target === "landscape" ? "Landscape" : "Portrait";\n    orientationBtn.setAttribute("aria-label", `Switch to ${target} orientation`);\n  }\n  async function toggleOrientation() {\n    const target = currentOrientation() === "portrait" ? "landscape" : "portrait";\n    if (window.WorldMetricsNative && typeof window.WorldMetricsNative.setOrientation === "function") {\n      window.WorldMetricsNative.setOrientation(target);\n      return;\n    }\n    try {\n      if (screen.orientation && typeof screen.orientation.lock === "function") {\n        await screen.orientation.lock(target);\n      }\n    } catch (_) {}\n  }'''
once(marker,replacement,'orientation helpers')

once('''  METRIC_KEYS.forEach((key) => {\n    const button = document.createElement("button");''','''  if (orientationBtn) orientationBtn.addEventListener("click", toggleOrientation);\n  window.addEventListener("resize", updateOrientationControl, { passive: true });\n  updateOrientationControl();\n\n  METRIC_KEYS.forEach((key) => {\n    const button = document.createElement("button");''','orientation listeners')

html_path.write_text(html,encoding='utf-8')

sw=ROOT/'www/service-worker.js'
if sw.exists():
    sw.write_text(sw.read_text(encoding='utf-8').replace('world-metrics-v1.0.1','world-metrics-v1.0.2'),encoding='utf-8')

for p in [ROOT/'package.json',ROOT/'package-lock.json']:
    if p.exists():
        d=json.loads(p.read_text(encoding='utf-8'))
        d['version']='1.0.2'
        if p.name=='package-lock.json' and '' in d.get('packages',{}): d['packages']['']['version']='1.0.2'
        p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')

main=ROOT/'android/app/src/main/java/app/worldmetrics/mobile/MainActivity.java'
main.write_text('''package app.worldmetrics.mobile;\n\nimport android.content.pm.ActivityInfo;\nimport android.content.res.Configuration;\nimport android.os.Bundle;\nimport android.webkit.JavascriptInterface;\n\nimport androidx.activity.OnBackPressedCallback;\n\nimport com.getcapacitor.BridgeActivity;\n\npublic class MainActivity extends BridgeActivity {\n    private OnBackPressedCallback worldMetricsBackCallback;\n\n    @Override\n    protected void onCreate(Bundle savedInstanceState) {\n        super.onCreate(savedInstanceState);\n        if (getBridge() != null && getBridge().getWebView() != null) {\n            getBridge().getWebView().addJavascriptInterface(new WorldMetricsNativeBridge(), "WorldMetricsNative");\n        }\n        worldMetricsBackCallback = new OnBackPressedCallback(true) {\n            @Override\n            public void handleOnBackPressed() {\n                if (getBridge() == null || getBridge().getWebView() == null) { finish(); return; }\n                getBridge().getWebView().evaluateJavascript(\n                    "(function(){try{return !!(window.__worldMetricsHandleBack && window.__worldMetricsHandleBack());}catch(e){return false;}})();",\n                    result -> {\n                        if (!"true".equals(result)) {\n                            setEnabled(false);\n                            getOnBackPressedDispatcher().onBackPressed();\n                            setEnabled(true);\n                        }\n                    }\n                );\n            }\n        };\n        getOnBackPressedDispatcher().addCallback(this, worldMetricsBackCallback);\n    }\n\n    private class WorldMetricsNativeBridge {\n        @JavascriptInterface\n        public void setOrientation(String orientation) {\n            runOnUiThread(() -> {\n                if ("landscape".equals(orientation)) setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);\n                else if ("portrait".equals(orientation)) setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);\n                else setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED);\n            });\n        }\n        @JavascriptInterface\n        public String getOrientation() {\n            int value = getResources().getConfiguration().orientation;\n            return value == Configuration.ORIENTATION_LANDSCAPE ? "landscape" : "portrait";\n        }\n    }\n}\n''',encoding='utf-8')

bg=ROOT/'android/app/build.gradle'
if bg.exists():
    t=bg.read_text(encoding='utf-8')
    t=re.sub(r'(?m)^\s*versionCode\s+2\s*$', '        versionCode 3', t, count=1)
    t=re.sub(r'(?m)^\s*versionName\s+"1\.0\.1"\s*$', '        versionName "1.0.2"', t, count=1)
    bg.write_text(t,encoding='utf-8')

au=ROOT/'scripts/static-audit.mjs'
if au.exists():
    t=au.read_text(encoding='utf-8')
    marker="  ['active metric auto-scrolls on mobile', html.includes('ensureMetricVisible') && html.includes('scrollIntoView')]"
    if "['orientation toggle'" not in t:
        if marker not in t: raise SystemExit('static audit marker missing')
        replacement=marker+",\n  ['metric row contained on mobile', html.includes('grid-template-columns: repeat(5, minmax(0, 1fr))')],\n  ['orientation toggle', html.includes('orientation-toggle') && mainActivity.includes('WorldMetricsNativeBridge') && mainActivity.includes('SCREEN_ORIENTATION_LANDSCAPE')],\n  ['flat map safe geometry fit', html.includes('flatFitObject') && html.includes('projection.fitExtent')],\n  ['device repair version 1.0.2', html.includes('data-app-version=\"1.0.2\"')]"
        t=t.replace(marker,replacement,1)
    au.write_text(t,encoding='utf-8')
print('Device QA Repair v2 applied')
