"""Regenerates assets/ (icon + splash artwork). Run: python3 scripts/make_icons.py  (needs Pillow)"""
import math, os
from PIL import Image, ImageDraw, ImageFont

S = 2048

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def background(size):
    img = Image.new('RGB', (size, size))
    px = img.load()
    c = size / 2
    inner, outer = (22, 62, 78), (5, 14, 21)
    for y in range(size):
        for x in range(size):
            d = min(1.0, math.hypot(x - c, y - c) / (size * 0.72))
            px[x, y] = lerp(inner, outer, d)
    return img

def rings(img, size):
    d = ImageDraw.Draw(img, 'RGBA')
    c = size / 2
    for r in (0.2, 0.34, 0.48):
        R = size * r
        d.ellipse([c - R, c - R, c + R, c + R], outline=(143, 232, 200, 70), width=max(2, size // 300))
    return img

def sweep(size, angle_deg=-48, half_deg=10, length=0.47):
    layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = size / 2
    R = size * length
    for k, a in enumerate((26, 38, 56)):
        h = half_deg * (1.5 - 0.5 * k)
        pts = [(c, c)]
        for i in range(0, 41):
            ang = math.radians(angle_deg - h + (2 * h) * i / 40)
            pts.append((c + R * math.cos(ang), c + R * math.sin(ang)))
        d.polygon(pts, fill=(143, 232, 200, a))
    return layer

def ship(size, scale=1.0):
    layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = size / 2
    L, Wd = size * 0.34 * scale, size * 0.095 * scale
    def P(x, y): return (c + y, c - x)
    # soft narrow wake
    for k, a in enumerate((34, 24, 14)):
        spread = Wd * (0.5 + 0.7 * k)
        d.polygon([P(-L / 2, -Wd * 0.3), P(-L / 2, Wd * 0.3), P(-L * (0.9 + 0.2 * k), spread), P(-L * (0.9 + 0.2 * k), -spread)], fill=(210, 232, 238, a))
    hull = [P(L / 2, 0), P(L * 0.32, -Wd * 0.45), P(L * 0.05, -Wd * 0.5), P(-L / 2 + 10, -Wd * 0.5), P(-L / 2, -Wd * 0.4),
            P(-L / 2, Wd * 0.4), P(-L / 2 + 10, Wd * 0.5), P(L * 0.05, Wd * 0.5), P(L * 0.32, Wd * 0.45)]
    d.polygon(hull, fill=(43, 57, 67, 255), outline=(0, 0, 0, 200))
    deck = [P(L * 0.46, 0), P(L * 0.3, -Wd * 0.34), P(L * 0.05, -Wd * 0.38), P(-L * 0.45, -Wd * 0.38), P(-L * 0.45, Wd * 0.38), P(L * 0.05, Wd * 0.38), P(L * 0.3, Wd * 0.34)]
    d.polygon(deck, fill=(111, 127, 136, 255))
    def rect(x0, x1, y0, y1, col):
        d.polygon([P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)], fill=col)
    rect(-L * 0.1, L * 0.09, -Wd * 0.3, Wd * 0.3, (141, 155, 163, 255))
    rect(-L * 0.28, -L * 0.14, -Wd * 0.24, Wd * 0.24, (75, 89, 98, 255))
    for i in range(4):
        x0 = L * 0.14 + i * L * 0.06
        rect(x0, x0 + L * 0.045, -Wd * 0.26, -Wd * 0.06, (56, 69, 77, 255))
        rect(x0, x0 + L * 0.045, Wd * 0.06, Wd * 0.26, (56, 69, 77, 255))
    gx, gy = P(L * 0.36, 0)
    r = Wd * 0.16
    d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(85, 100, 109, 255))
    d.line([P(L * 0.36, 0), P(L * 0.36 + L * 0.12, 0)], fill=(42, 52, 58, 255), width=max(2, int(size * 0.006)))
    return layer

def compose(with_bg, ship_scale):
    img = background(S).convert('RGBA') if with_bg else Image.new('RGBA', (S, S), (0, 0, 0, 0))
    if with_bg:
        img = rings(img, S)
    img.alpha_composite(sweep(S))
    img.alpha_composite(ship(S, ship_scale))
    return img

os.makedirs('assets', exist_ok=True)
full = compose(True, 1.55).convert('RGB').resize((1024, 1024), Image.LANCZOS)
full.save('assets/icon-only.png')
compose(False, 1.25).resize((1024, 1024), Image.LANCZOS).save('assets/icon-foreground.png')
rings(background(S).convert('RGBA'), S).convert('RGB').resize((1024, 1024), Image.LANCZOS).save('assets/icon-background.png')

SP = 2732
for name in ('splash.png', 'splash-dark.png'):
    sp = Image.new('RGB', (SP, SP), (7, 18, 26))
    mark = full.resize((900, 900), Image.LANCZOS)
    mask = Image.new('L', (900, 900), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 899, 899], radius=190, fill=255)
    sp.paste(mark, ((SP - 900) // 2, (SP - 900) // 2 - 80), mask)
    d = ImageDraw.Draw(sp)
    try:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 110)
        w = d.textlength('PICKET SHIP', font=f)
        d.text(((SP - w) / 2, (SP + 900) // 2 - 20), 'PICKET SHIP', font=f, fill=(219, 231, 230))
    except Exception as e:
        print('no font, splash has no title:', e)
    sp.save('assets/' + name)

full.resize((512, 512), Image.LANCZOS).save('assets/preview-icon.png')
print(sorted(os.listdir('assets')))
