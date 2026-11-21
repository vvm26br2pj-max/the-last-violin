"""Draws the home-screen icons: a glowing gold violin on a night-purple field.
Run: python3 make_icons.py  (writes icon-180.png, icon-192.png, icon-512.png)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).parent
S = 1024
CLEAR = (0, 0, 0, 0)


def background():
    bg = Image.new('RGB', (S, S), '#07050c')
    d = ImageDraw.Draw(bg)
    for r in range(S, 0, -8):
        t = r / S
        d.ellipse([S / 2 - r * .75, S / 2 - r * .75, S / 2 + r * .75, S / 2 + r * .75],
                  fill=(int(7 + 60 * (1 - t)), int(5 + 40 * (1 - t)), int(12 + 80 * (1 - t))))
    return bg


def violin():
    v = Image.new('RGBA', (S, S), CLEAR)
    g = ImageDraw.Draw(v)
    gold, dark, wood = '#f2c14e', '#3b1f0c', '#c98a22'
    cx = S // 2
    g.ellipse([cx - 210, 560, cx + 210, 900], fill=gold)      # lower bout
    g.ellipse([cx - 170, 330, cx + 170, 630], fill=gold)      # upper bout
    g.rectangle([cx - 150, 560, cx + 150, 650], fill=gold)
    for sx in (-1, 1):                                        # C-bout waist curves
        x = cx + sx * 190
        g.ellipse([x - 70, 545, x + 70, 665], fill=CLEAR)
        g.line([(cx + sx * 92, 640), (cx + sx * 80, 720), (cx + sx * 98, 800)], fill=dark, width=16, joint='curve')  # f-holes
    g.rectangle([cx - 30, 120, cx + 30, 570], fill=wood)      # neck
    g.ellipse([cx - 52, 70, cx + 52, 174], fill=wood)        # scroll
    g.ellipse([cx - 22, 100, cx + 22, 144], fill=dark)
    g.rectangle([cx - 66, 822, cx + 66, 846], fill=dark)      # bridge
    for k in (-18, -6, 6, 18):                                # strings
        g.line([(cx + k * .7, 150), (cx + k * 1.5, 834)], fill='#fff3c8', width=4)
    return v.rotate(-28, resample=Image.BICUBIC, center=(cx, S // 2))


bg, v = background(), violin()
glow = v.filter(ImageFilter.GaussianBlur(28))
bg.paste((242, 193, 78), mask=glow.split()[3].point(lambda a: a * .55))
bg.paste(v, mask=v.split()[3])
for n in (180, 192, 512):
    bg.resize((n, n), Image.LANCZOS).save(HERE / f'icon-{n}.png')
print('icons written')
