"""Carrossel GTA Loucura v2 (1080x1350, 4:5) no estilo das letras aprovadas, com fundo de Vice City.

Uso: python3 carrossel_v2_skyline.py slides.json pasta_saida
slides.json: {"fundo": "caminho.png", "slides": [{"titulo_1","titulo_2","sub":[linhas],"foto","credito_foto","cta_1","cta_2"}]}
Sem contador de páginas (o Instagram já mostra).
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v3 import brilho, RAIZ, PINK, CYAN, WHITE

W, H = 1080, 1350
INTER = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
INTER_IT = '/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf'
F = lambda p, s: ImageFont.truetype(p, s)

def caber(d, t, p, smax, smin, larg):
    s = smax
    while s > smin and d.textlength(t, font=F(p, s)) > larg: s -= 2
    return F(p, s)

def fundo(path):
    im = Image.new('RGBA', (W, H), (12, 4, 26, 255))
    bg = Image.open(path).convert('RGBA'); r = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * r) + 1, int(bg.height * r) + 1), Image.LANCZOS)
    x0 = (bg.width - W) // 2; y0 = bg.height - H
    im.alpha_composite(bg.crop((x0, y0, x0 + W, y0 + H)))
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for y in range(H):  # escurece mais no topo (texto) e menos embaixo (cidade aparece)
        a = int(200 - 120 * min(1, max(0, (y - 500) / 850)))
        gd.line([(0, y), (W, y)], fill=(10, 2, 24, a))
    im.alpha_composite(g)
    return im

def texto(im, xy, t, f, cor, anchor='lm', glow=None):
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(c).text((xy[0] + 4, xy[1] + 5), t, font=f, fill=(8, 0, 20, 220), anchor=anchor)
    im.alpha_composite(c.filter(ImageFilter.GaussianBlur(3)))
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(c).text(xy, t, font=f, fill=(*cor, 255), anchor=anchor)
    brilho(im, c, glow, 1) if glow else im.alpha_composite(c)

def faixa_rosa(im, y, linhas, tam=40):
    d = ImageDraw.Draw(im); f = F(INTER_IT, tam); lh = int(tam * 1.12)
    larg = max(d.textlength(l, font=f) for l in linhas)
    x0, x1, y0, y1, sk = 96, 96 + larg + 70, y, y + lh * len(linhas) + 26, 26
    d.polygon([(x0 + sk, y0), (x1 + sk, y0), (x1 - sk, y1), (x0 - sk, y1)], fill=PINK)
    d.polygon([(x0 - sk - 30, y0), (x0 - sk - 16, y0), (x0 - sk - 46, y1), (x0 - sk - 60, y1)], fill=CYAN)
    for i, l in enumerate(linhas):
        d.text((x0 + 30 - i * 6, y0 + 13 + i * lh), l, font=f, fill=WHITE)
    return y1

def slide(s, fundo_path):
    im = fundo(fundo_path); d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(RAIZ, 'logo', 'plaquinha-gta-loucura.png'))
    lw = 200; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    im.alpha_composite(logo, (44, 36))
    d.rounded_rectangle([270, 92, 1036, 96], radius=2, fill=CYAN)
    y = 238
    if s.get('titulo_1'):
        texto(im, (W / 2, y), s['titulo_1'], caber(d, s['titulo_1'], INTER, 96, 40, 980), WHITE, 'mm'); y += 104
    if s.get('titulo_2'):
        texto(im, (W / 2, y), s['titulo_2'], caber(d, s['titulo_2'], INTER_IT, 112, 40, 990), PINK, 'mm', glow=10); y += 84
    if s.get('sub'): y = faixa_rosa(im, y, s['sub']) + 26
    if s.get('foto'):
        ft = Image.open(s['foto']).convert('RGBA')
        import numpy as np  # corta faixas pretas (letterbox) da foto
        a = np.asarray(ft.convert('L')); lin = np.where(a.mean(axis=1) > 14)[0]
        if len(lin): ft = ft.crop((0, int(lin.min()), ft.width, int(lin.max()) + 1))
        bh = 1180 - y if s.get('cta_1') else 1240 - y
        bw = W - 88; r = max(bw / ft.width, bh / ft.height)
        ft = ft.resize((int(ft.width * r) + 1, int(ft.height * r) + 1), Image.LANCZOS)
        ft = ft.crop(((ft.width - bw) // 2, (ft.height - bh) // 2, (ft.width - bw) // 2 + bw, (ft.height - bh) // 2 + bh))
        m = Image.new('L', (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw, bh], radius=22, fill=255)
        im.paste(ft, (44, y), m)
        fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(fr).rounded_rectangle([42, y - 2, 46 + bw, y + bh + 2], radius=24, outline=(*CYAN, 255), width=4)
        brilho(im, fr, 10, 1); d = ImageDraw.Draw(im)
        if s.get('credito_foto'):
            f = F(INTER, 20); tw = d.textlength(s['credito_foto'], font=f)
            d.rounded_rectangle([W - 60 - tw - 28, y + bh - 50, W - 60, y + bh - 16], radius=17, fill=(10, 4, 24, 220))
            d.text((W - 60 - tw - 14, y + bh - 33), s['credito_foto'], font=f, fill=(225, 215, 240), anchor='lm')
        y += bh + 20
    if s.get('cta_1'):
        d.polygon([(52, y + 6), (62, y + 6), (54, y + 60), (44, y + 60)], fill=CYAN)
        texto(im, (78, y + 34), s['cta_1'], caber(d, s['cta_1'], INTER_IT, 60, 30, 940), WHITE)
    d.rounded_rectangle([60, 1272, 820, 1276], radius=2, fill=CYAN)
    texto(im, (64, 1306), '@gta6_loucura', F(INTER_IT, 34), WHITE)
    return im.convert('RGB')

if __name__ == '__main__':
    r = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    for i, s in enumerate(r['slides'], 1):
        slide(s, r['fundo']).save(os.path.join(out, f'slide-{i:02d}.jpg'), quality=93)
    print('ok', len(r['slides']))
