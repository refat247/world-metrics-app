from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, re

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'android/app/src/main/res'

BG = '#0B1118'
CYAN = '#48CBC7'
CYAN_SOFT = '#A7E9E3'
AMBER = '#E6AD4F'
MUTED = '#6F8795'
WHITE = '#F4F7F8'


def font(size, bold=False):
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf',
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def draw_mark(draw, box, stroke, include_bars=True):
    x0, y0, x1, y1 = box
    w = x1 - x0
    cx, cy = (x0+x1)/2, (y0+y1)/2
    r = w * 0.38
    lw = max(2, int(w * 0.055))
    globe = [cx-r, cy-r, cx+r, cy+r]
    draw.ellipse(globe, outline=CYAN, width=lw)
    draw.ellipse([cx-r*0.56, cy-r, cx+r*0.56, cy+r], outline=CYAN_SOFT, width=max(1, lw//2))
    draw.ellipse([cx-r*0.23, cy-r, cx+r*0.23, cy+r], outline=CYAN_SOFT, width=max(1, lw//2))
    draw.arc([cx-r, cy-r*0.55, cx+r, cy+r*0.55], 0, 180, fill=CYAN_SOFT, width=max(1, lw//2))
    draw.arc([cx-r, cy-r*0.55, cx+r, cy+r*0.55], 180, 360, fill=CYAN_SOFT, width=max(1, lw//2))
    if include_bars:
        bx = cx + r*0.18
        by = cy + r*0.55
        bw = r*0.20
        gap = bw*0.35
        heights = [r*0.28, r*0.48, r*0.72]
        colors = [MUTED, CYAN, AMBER]
        for i, (h, c) in enumerate(zip(heights, colors)):
            xx = bx + i*(bw+gap)
            draw.rounded_rectangle([xx, by-h, xx+bw, by], radius=max(1,int(bw*0.18)), fill=c)


def launcher(size, round_icon=False):
    im = Image.new('RGBA', (size, size), (0,0,0,0) if round_icon else BG)
    d = ImageDraw.Draw(im)
    if round_icon:
        d.ellipse([0,0,size-1,size-1], fill=BG)
    else:
        rad = int(size*0.20)
        d.rounded_rectangle([0,0,size-1,size-1], radius=rad, fill=BG)
    pad = size*0.11
    draw_mark(d, [pad,pad,size-pad,size-pad], size)
    return im


def foreground(size):
    im = Image.new('RGBA', (size,size), (0,0,0,0))
    d = ImageDraw.Draw(im)
    pad = size*0.19
    draw_mark(d, [pad,pad,size-pad,size-pad], size)
    return im


def splash(width, height):
    im = Image.new('RGB', (width,height), BG)
    d = ImageDraw.Draw(im)
    short = min(width,height)
    mark_size = int(short*0.36)
    cx = width//2
    cy = int(height*0.44)
    draw_mark(d, [cx-mark_size//2, cy-mark_size//2, cx+mark_size//2, cy+mark_size//2], mark_size)
    title_size = max(18, int(short*0.055))
    sub_size = max(10, int(short*0.024))
    title_font = font(title_size, True)
    sub_font = font(sub_size, False)
    title='WORLD METRICS'
    sub='GLOBAL INDICATORS · OFFLINE'
    tb=d.textbbox((0,0),title,font=title_font)
    sb=d.textbbox((0,0),sub,font=sub_font)
    d.text((cx-(tb[2]-tb[0])/2, cy+mark_size*0.62), title, fill=WHITE, font=title_font)
    d.text((cx-(sb[2]-sb[0])/2, cy+mark_size*0.62+title_size*1.35), sub, fill=MUTED, font=sub_font)
    return im


def save_png(im, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, format='PNG', optimize=True)

scales = {'mdpi':1.0,'hdpi':1.5,'xhdpi':2.0,'xxhdpi':3.0,'xxxhdpi':4.0}
for name, scale in scales.items():
    out = RES / f'mipmap-{name}'
    save_png(launcher(round(48*scale), False), out/'ic_launcher.png')
    save_png(launcher(round(48*scale), True), out/'ic_launcher_round.png')
    save_png(foreground(round(108*scale)), out/'ic_launcher_foreground.png')

for name, scale in scales.items():
    pw, ph = round(320*scale), round(480*scale)
    lw, lh = ph, pw
    save_png(splash(pw,ph), RES/f'drawable-port-{name}'/'splash.png')
    save_png(splash(lw,lh), RES/f'drawable-land-{name}'/'splash.png')
save_png(splash(640,960), RES/'drawable'/'splash.png')

store = ROOT/'artifacts/store'
store.mkdir(parents=True, exist_ok=True)
save_png(launcher(512, False), store/'google-play-icon-512.png')

(RES/'values/ic_launcher_background.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#0B1118</color>\n</resources>\n''', encoding='utf-8')

for p in [ROOT/'package.json', ROOT/'package-lock.json']:
    data=json.loads(p.read_text(encoding='utf-8'))
    data['version']='1.0.3'
    if p.name=='package-lock.json' and '' in data.get('packages',{}):
        data['packages']['']['version']='1.0.3'
    p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

html=ROOT/'www/index.html'
t=html.read_text(encoding='utf-8').replace('data-app-version="1.0.2"','data-app-version="1.0.3"',1)
html.write_text(t,encoding='utf-8')

sw=ROOT/'www/service-worker.js'
if sw.exists():
    sw.write_text(sw.read_text(encoding='utf-8').replace('world-metrics-v1.0.2','world-metrics-v1.0.3'),encoding='utf-8')

bg=ROOT/'android/app/build.gradle'
t=bg.read_text(encoding='utf-8')
t=re.sub(r'(?m)^\s*versionCode\s+3\s*$', '        versionCode 4', t, count=1)
t=re.sub(r'(?m)^\s*versionName\s+"1\.0\.2"\s*$', '        versionName "1.0.3"', t, count=1)
bg.write_text(t,encoding='utf-8')

# static-audit.mjs derives the expected app version from package.json.
print('World Metrics release branding generated; version=1.0.3 code=4')
