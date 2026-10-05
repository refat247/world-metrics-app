from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'scripts' / 'static-audit.mjs'
s = p.read_text(encoding='utf-8')
old = "['device repair version', html.includes('data-app-version=\\\"1.0.1\\\"')]"
new = "['device repair version', html.includes('data-app-version=\\\"1.0.2\\\"')]"
if old in s:
    s = s.replace(old, new, 1)
elif new not in s:
    raise SystemExit('legacy device repair version audit marker missing')
p.write_text(s, encoding='utf-8')
print('Legacy device-repair version audit updated to 1.0.2')
