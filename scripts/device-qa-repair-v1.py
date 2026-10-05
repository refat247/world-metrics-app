from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1] if Path(__file__).parent.name == 'scripts' else Path.cwd()
html_path = ROOT / 'www' / 'index.html'
html = html_path.read_text(encoding='utf-8')

if 'data-app-version="1.0.1"' not in html:
    def replace_once(old: str, new: str, label: str):
        global html
        if old not in html:
            raise SystemExit(f'Expected source block not found: {label}')
        html = html.replace(old, new, 1)

    replace_once(
        '.metric-switcher {\n  max-width: 100%;\n  overflow-x: auto;\n  scrollbar-width: none;\n}',
        '.metric-switcher {\n  max-width: 100%;\n  overflow-x: auto;\n  scrollbar-width: none;\n  scroll-behavior: smooth;\n  overscroll-behavior-x: contain;\n}',
        'metric switcher css',
    )

    toast_css = '''\n.back-toast {\n  position: fixed;\n  z-index: 100;\n  left: 50%;\n  bottom: max(22px, calc(env(safe-area-inset-bottom) + 14px));\n  transform: translate(-50%, 12px);\n  padding: 9px 13px;\n  border: 1px solid var(--color-line);\n  border-radius: 8px;\n  background: rgba(18, 24, 31, 0.96);\n  color: var(--color-fg);\n  font-family: var(--font-mono);\n  font-size: 11px;\n  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);\n  opacity: 0;\n  pointer-events: none;\n  transition: opacity 0.16s ease, transform 0.16s ease;\n}\n\n.back-toast.visible {\n  opacity: 1;\n  transform: translate(-50%, 0);\n}\n\n'''
    replace_once('@media (prefers-reduced-motion: reduce) {', toast_css + '@media (prefers-reduced-motion: reduce) {', 'back toast css')

    old_mobile = '''  .metric-btn,\n  .mode-btn {\n    min-height: 44px;\n    padding: 8px 12px;\n  }\n\n  .side-panel,\n  .panel-open .side-panel {\n    position: absolute;\n    z-index: 30;\n    left: 0;\n    right: 0;\n    bottom: 0;\n    width: 100%;\n    height: min(40vh, 340px);\n    border-left-width: 0;\n    border-top: 1px solid var(--color-line);\n    transform: translateY(100%);\n    transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1);\n  }\n\n  .panel-open .side-panel {\n    transform: translateY(0);\n  }\n\n  .panel-inner {\n    width: 100%;\n  }\n\n  .panel-open .zoom-controls,\n  .panel-open .reset-view {\n    bottom: calc(min(40vh, 340px) + 10px);\n  }\n}'''
    new_mobile = '''  .metric-switcher {\n    scroll-snap-type: x proximity;\n  }\n\n  .metric-btn,\n  .mode-btn {\n    min-height: 44px;\n    padding: 8px 12px;\n  }\n\n  .metric-btn {\n    flex: 0 0 auto;\n    scroll-snap-align: center;\n  }\n\n  .legend {\n    left: 8px;\n    top: 8px;\n    width: min(188px, 50vw);\n    padding: 8px 10px;\n  }\n\n  .legend-title {\n    margin: 2px 0 5px;\n    font-size: 12px;\n  }\n\n  .legend-note {\n    display: none;\n  }\n\n  .key-row {\n    margin-top: 5px;\n    font-size: 9px;\n  }\n\n  .side-panel,\n  .panel-open .side-panel {\n    position: absolute;\n    z-index: 30;\n    left: 0;\n    right: 0;\n    bottom: 0;\n    width: 100%;\n    height: min(44dvh, 360px);\n    max-height: calc(100% - 116px);\n    border-left-width: 0;\n    border-top: 1px solid var(--color-line);\n    transform: translateY(100%);\n    transition: transform 0.24s cubic-bezier(0.22, 1, 0.36, 1);\n  }\n\n  .panel-open .side-panel {\n    transform: translateY(0);\n  }\n\n  .panel-inner {\n    width: 100%;\n  }\n\n  .panel-open .zoom-controls {\n    bottom: calc(min(44dvh, 360px) + 10px);\n  }\n\n  .panel-open .reset-view {\n    opacity: 0;\n    pointer-events: none;\n  }\n}'''
    replace_once(old_mobile, new_mobile, 'mobile css')

    replace_once(
        '  let lastSpin = 0;\n  let raf = 0;\n  let lastWidth = 0;\n  let focusTimer = 0;',
        '  let lastSpin = 0;\n  let raf = 0;\n  let globePaintRaf = 0;\n  let lastWidth = 0;\n  let focusTimer = 0;\n  let lastRootBack = 0;\n  let backToastTimer = 0;',
        'runtime variables',
    )

    old_paint = '''  function paintGlobe() {\n    globeProjection.rotate([globeRotation[0], globeRotation[1], 0]).scale(globeBaseScale * globeScale0).translate([width / 2, centerY()]);\n    countriesG.selectAll("path.country").attr("d", globePath);\n    sphere.attr("d", globePath({ type: "Sphere" }));\n    sphereG.select(".graticule").attr("d", globePath(graticule));\n    d3.select(clipPath).attr("d", globePath({ type: "Sphere" }));\n  }'''
    new_paint = '''  function paintGlobe() {\n    globeProjection.rotate([globeRotation[0], globeRotation[1], 0]).scale(globeBaseScale * globeScale0).translate([width / 2, centerY()]);\n    countriesG.selectAll("path.country").attr("d", globePath);\n    sphere.attr("d", globePath({ type: "Sphere" }));\n    sphereG.select(".graticule").attr("d", globePath(graticule));\n    d3.select(clipPath).attr("d", globePath({ type: "Sphere" }));\n  }\n  function scheduleGlobePaint() {\n    if (globePaintRaf) return;\n    globePaintRaf = requestAnimationFrame(() => {\n      globePaintRaf = 0;\n      paintGlobe();\n    });\n  }\n  function setGlobePreviewScale(ratio) {\n    const cx = width / 2;\n    const cy = centerY();\n    const transform = `translate(${cx} ${cy}) scale(${ratio}) translate(${-cx} ${-cy})`;\n    zoomRoot.attr("transform", transform);\n    d3.select(clipPath).attr("transform", transform);\n  }\n  function clearGlobePreviewScale() {\n    zoomRoot.attr("transform", null);\n    d3.select(clipPath).attr("transform", null);\n  }'''
    replace_once(old_paint, new_paint, 'globe paint scheduler')

    old_fit = '''    projection.fitExtent(\n      [\n        [8, 8],\n        [Math.max(16, width - 8), Math.max(16, height - 8)],\n      ],\n      { type: "Sphere" },\n    );'''
    new_fit = old_fit + '''\n    if (isMobile() && height > width) {\n      projection.scale(projection.scale() * 1.12).translate([width / 2, height * 0.44]);\n    }'''
    replace_once(old_fit, new_fit, 'mobile flat fit')

    replace_once(
        '      globeRotation = [rotation[0] + event.dx * sensitivity, Math.max(-90, Math.min(90, rotation[1] - event.dy * sensitivity))];\n      paintGlobe();',
        '      globeRotation = [rotation[0] + event.dx * sensitivity, Math.max(-90, Math.min(90, rotation[1] - event.dy * sensitivity))];\n      scheduleGlobePaint();',
        'drag redraw coalescing',
    )

    replace_once(
        '    globeScale0 = Math.max(0.8, Math.min(8, globeScale0 * factor));\n    paintGlobe();\n    setReadout(Math.round(globeScale0 * 100) + "%");',
        '    globeScale0 = Math.max(0.8, Math.min(8, globeScale0 * factor));\n    scheduleGlobePaint();\n    setReadout(Math.round(globeScale0 * 100) + "%");',
        'wheel redraw coalescing',
    )

    old_pinch = '''  let pinchDistance = 0;\n  function touchDistance(touches) {\n    const a = touches[0];\n    const b = touches[1];\n    if (!a || !b) return 0;\n    return Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY);\n  }\n  function onTouchStart(event) {\n    if (event.touches.length === 2) pinchDistance = touchDistance(event.touches);\n  }\n  function onTouchMove(event) {\n    if (mode !== "globe" || event.touches.length !== 2) return;\n    event.preventDefault();\n    const next = touchDistance(event.touches);\n    if (pinchDistance > 0 && next > 0) {\n      globeScale0 = Math.max(0.8, Math.min(8, globeScale0 * (next / pinchDistance)));\n      paintGlobe();\n      setReadout(Math.round(globeScale0 * 100) + "%");\n      pauseSpin(6000);\n    }\n    pinchDistance = next;\n  }\n  svg.addEventListener("wheel", onWheel, { passive: false });\n  svg.addEventListener("touchstart", onTouchStart, { passive: true });\n  svg.addEventListener("touchmove", onTouchMove, { passive: false });'''
    new_pinch = '''  let pinchStartDistance = 0;\n  let pinchStartScale = 1;\n  let pinchTargetScale = 1;\n  function touchDistance(touches) {\n    const a = touches[0];\n    const b = touches[1];\n    if (!a || !b) return 0;\n    return Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY);\n  }\n  function onTouchStart(event) {\n    if (mode !== "globe" || event.touches.length !== 2) return;\n    pinchStartDistance = touchDistance(event.touches);\n    pinchStartScale = globeScale0;\n    pinchTargetScale = globeScale0;\n    pauseSpin(6000);\n  }\n  function onTouchMove(event) {\n    if (mode !== "globe" || event.touches.length !== 2 || pinchStartDistance <= 0) return;\n    event.preventDefault();\n    const next = touchDistance(event.touches);\n    if (next <= 0) return;\n    pinchTargetScale = Math.max(0.8, Math.min(8, pinchStartScale * (next / pinchStartDistance)));\n    setGlobePreviewScale(pinchTargetScale / pinchStartScale);\n    setReadout(Math.round(pinchTargetScale * 100) + "%");\n  }\n  function onTouchEnd(event) {\n    if (mode !== "globe" || pinchStartDistance <= 0 || event.touches.length >= 2) return;\n    globeScale0 = pinchTargetScale;\n    pinchStartDistance = 0;\n    clearGlobePreviewScale();\n    paintGlobe();\n    setReadout(Math.round(globeScale0 * 100) + "%");\n    pauseSpin(6000);\n  }\n  svg.addEventListener("wheel", onWheel, { passive: false });\n  svg.addEventListener("touchstart", onTouchStart, { passive: true });\n  svg.addEventListener("touchmove", onTouchMove, { passive: false });\n  svg.addEventListener("touchend", onTouchEnd, { passive: true });\n  svg.addEventListener("touchcancel", onTouchEnd, { passive: true });'''
    replace_once(old_pinch, new_pinch, 'pinch preview')

    replace_once(
        '    globeRotation = [globeRotation[0] + dt * 6, globeRotation[1]];\n    paintGlobe();',
        '    globeRotation = [globeRotation[0] + dt * 6, globeRotation[1]];\n    scheduleGlobePaint();',
        'spin redraw coalescing',
    )

    replace_once(
        '  function setMode(next) {\n    if (next === mode) return;\n    mode = next;',
        '  function setMode(next) {\n    if (next === mode) return;\n    clearGlobePreviewScale();\n    pinchStartDistance = 0;\n    mode = next;',
        'mode clears pinch preview',
    )

    helpers = '''  function ensureMetricVisible(button) {\n    if (!button || !isMobile()) return;\n    button.scrollIntoView({ behavior: reducedMotion() ? "auto" : "smooth", block: "nearest", inline: "center" });\n  }\n  function showBackToast() {\n    let toast = document.getElementById("back-toast");\n    if (!toast) {\n      toast = document.createElement("div");\n      toast.id = "back-toast";\n      toast.className = "back-toast";\n      toast.setAttribute("role", "status");\n      toast.textContent = "Press back again to exit";\n      document.body.appendChild(toast);\n    }\n    toast.classList.add("visible");\n    window.clearTimeout(backToastTimer);\n    backToastTimer = window.setTimeout(() => toast.classList.remove("visible"), 1600);\n  }\n  window.__worldMetricsHandleBack = function () {\n    if (document.activeElement === queryEl || searchOpen) {\n      searchOpen = false;\n      query = "";\n      queryEl.value = "";\n      queryEl.blur();\n      renderResults();\n      return true;\n    }\n    if (selected) {\n      chooseSelection(null, false);\n      return true;\n    }\n    const now = Date.now();\n    if (now - lastRootBack < 1800) return false;\n    lastRootBack = now;\n    showBackToast();\n    return true;\n  };\n\n'''
    replace_once('  function renderPanel() {', helpers + '  function renderPanel() {', 'back and metric helpers')

    old_render_legend = '''    metricHost.querySelectorAll(".metric-btn").forEach((button) => {\n      button.setAttribute("aria-checked", button.getAttribute("data-metric") === metric ? "true" : "false");\n    });'''
    new_render_legend = '''    metricHost.querySelectorAll(".metric-btn").forEach((button) => {\n      const active = button.getAttribute("data-metric") === metric;\n      button.setAttribute("aria-checked", active ? "true" : "false");\n      if (active) requestAnimationFrame(() => ensureMetricVisible(button));\n    });'''
    replace_once(old_render_legend, new_render_legend, 'active metric visibility')

    old_choose = '''  function choose(entry) {\n    query = "";\n    queryEl.value = "";\n    searchOpen = false;\n    renderResults();\n    chooseSelection({ iso: entry.iso, name: entry.name }, true);\n  }'''
    new_choose = '''  function choose(entry) {\n    query = "";\n    queryEl.value = "";\n    searchOpen = false;\n    renderResults();\n    queryEl.blur();\n    requestAnimationFrame(() => chooseSelection({ iso: entry.iso, name: entry.name }, true));\n  }'''
    replace_once(old_choose, new_choose, 'keyboard dismissal')

    old_metric_click = '''      renderLegend();\n      paintFills(true);\n      renderPanel();\n    });'''
    new_metric_click = '''      renderLegend();\n      paintFills(true);\n      renderPanel();\n      ensureMetricVisible(button);\n    });'''
    replace_once(old_metric_click, new_metric_click, 'metric click visibility')

    old_escape = '''  window.addEventListener("keydown", (event) => {\n    if (event.key !== "Escape") return;\n    searchOpen = false;\n    renderResults();\n    chooseSelection(null, false);\n  });'''
    new_escape = '''  window.addEventListener("keydown", (event) => {\n    if (event.key !== "Escape") return;\n    window.__worldMetricsHandleBack();\n  });'''
    replace_once(old_escape, new_escape, 'escape/back parity')

    html = html.replace('data-app-version="1.0.0"', 'data-app-version="1.0.1"', 1)
    html_path.write_text(html, encoding='utf-8')
else:
    print('HTML repair already applied')

sw = ROOT / 'www' / 'service-worker.js'
if sw.exists():
    sw.write_text(sw.read_text(encoding='utf-8').replace('world-metrics-v1.0.0', 'world-metrics-v1.0.1'), encoding='utf-8')

package = ROOT / 'package.json'
if package.exists():
    data = json.loads(package.read_text(encoding='utf-8')); data['version'] = '1.0.1'
    package.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

lock = ROOT / 'package-lock.json'
if lock.exists():
    data = json.loads(lock.read_text(encoding='utf-8')); data['version'] = '1.0.1'
    if '' in data.get('packages', {}): data['packages']['']['version'] = '1.0.1'
    lock.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

main_activity = ROOT / 'android' / 'app' / 'src' / 'main' / 'java' / 'app' / 'worldmetrics' / 'mobile' / 'MainActivity.java'
main_activity.parent.mkdir(parents=True, exist_ok=True)
main_activity.write_text('''package app.worldmetrics.mobile;\n\nimport android.os.Bundle;\n\nimport androidx.activity.OnBackPressedCallback;\n\nimport com.getcapacitor.BridgeActivity;\n\npublic class MainActivity extends BridgeActivity {\n    private OnBackPressedCallback worldMetricsBackCallback;\n\n    @Override\n    protected void onCreate(Bundle savedInstanceState) {\n        super.onCreate(savedInstanceState);\n\n        worldMetricsBackCallback = new OnBackPressedCallback(true) {\n            @Override\n            public void handleOnBackPressed() {\n                if (getBridge() == null || getBridge().getWebView() == null) {\n                    finish();\n                    return;\n                }\n\n                getBridge().getWebView().evaluateJavascript(\n                    "(function(){try{return !!(window.__worldMetricsHandleBack && window.__worldMetricsHandleBack());}catch(e){return false;}})();",\n                    result -> {\n                        if (!"true".equals(result)) {\n                            setEnabled(false);\n                            getOnBackPressedDispatcher().onBackPressed();\n                            setEnabled(true);\n                        }\n                    }\n                );\n            }\n        };\n\n        getOnBackPressedDispatcher().addCallback(this, worldMetricsBackCallback);\n    }\n}\n''', encoding='utf-8')

build_gradle = ROOT / 'android' / 'app' / 'build.gradle'
if build_gradle.exists():
    text = build_gradle.read_text(encoding='utf-8')
    text = re.sub(r'(?m)^\s*versionCode\s+1\s*$', '        versionCode 2', text, count=1)
    text = re.sub(r'(?m)^\s*versionName\s+"1\.0"\s*$', '        versionName "1.0.1"', text, count=1)
    build_gradle.write_text(text, encoding='utf-8')

audit = ROOT / 'scripts' / 'static-audit.mjs'
if audit.exists():
    text = audit.read_text(encoding='utf-8')
    activity_line = "const mainActivity = fs.readFileSync(new URL('../android/app/src/main/java/app/worldmetrics/mobile/MainActivity.java', import.meta.url), 'utf8');"
    if activity_line not in text:
        manifest_line = "const manifest = JSON.parse(fs.readFileSync(new URL('../www/manifest.webmanifest', import.meta.url), 'utf8'));"
        if manifest_line not in text: raise SystemExit('static audit manifest marker missing')
        text = text.replace(manifest_line, manifest_line + '\n' + activity_line, 1)
    if "['native back bridge'" not in text:
        marker = "  ['manifest icons', Array.isArray(manifest.icons) && manifest.icons.length >= 3]"
        replacement = marker + ",\n  ['native back bridge', mainActivity.includes('OnBackPressedCallback') && mainActivity.includes('__worldMetricsHandleBack')],\n  ['web back priority handler', html.includes('window.__worldMetricsHandleBack') && html.includes('Press back again to exit')],\n  ['search selection dismisses keyboard', html.includes('queryEl.blur()')],\n  ['pinch zoom uses preview transform', html.includes('setGlobePreviewScale') && html.includes('pinchTargetScale')],\n  ['globe redraws coalesced', html.includes('scheduleGlobePaint') && html.includes('globePaintRaf')],\n  ['active metric auto-scrolls on mobile', html.includes('ensureMetricVisible') && html.includes('scrollIntoView')],\n  ['device repair version', html.includes('data-app-version=\\\"1.0.1\\\"')]"
        if marker not in text: raise SystemExit('static audit checks marker missing')
        text = text.replace(marker, replacement, 1)
    audit.write_text(text, encoding='utf-8')

print('Device QA Repair v1 applied successfully')
