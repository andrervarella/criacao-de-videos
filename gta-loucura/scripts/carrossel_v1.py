"""Carrossel GTA Loucura (1080x1350, 4:5) a partir de um JSON de slides.

Uso: python3 carrossel_v1.py slides.json pasta_saida
Cada slide: {"tipo": "capa"|"numero"|"texto"|"cta", ...}. Veja um exemplo em
videos/2026-11-20-carrossel-bilhoes/slides.json.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.join(AQUI, '..')
W, H = 1080, 1350
PINK = (255, 36, 145); CYAN = (45, 230, 240); WHITE = (255, 255, 255); DARK = (22, 6, 36); GOLD = (255, 205, 80)
MI = '/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat-Italic[wght].ttf'
MR = '/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf'

def fonte(s, w='Black', it=True):
    f = ImageFont.truetype(MI if it else MR, s); f.set_variation_by_name(f'{w} Italic' if it else w); return f

def caber(d, txt, w, smax, larg, smin=30, it=True):
    s = smax
    while s > smin and d.textlength(txt, font=fonte(s, w, it)) > larg: s -= 2
    return fonte(s, w, it)

def quebrar(d, txt, f, larg):
    linhas, atual = [], ''
    for p in txt.split():
        t = (atual + ' ' + p).strip()
        if d.textlength(t, font=f) <= larg: atual = t
        else: linhas.append(atual); atual = p
    return linhas + ([atual] if atual else [])

def brilho(base, camada, r=16, n=2):
    g = camada.filter(ImageFilter.GaussianBlur(r))
    for _ in range(n): base.alpha_composite(g)
    base.alpha_composite(camada)

def fundo(foco_y=0.55, escurecer=150):
    bg = Image.open(os.path.join(RAIZ, 'fundos', 'fundo-vice-neon-v1.png')).convert('RGBA')
    s = W / bg.width * 1.15; bg = bg.resize((int(bg.width * s), int(bg.height * s)), Image.LANCZOS)
    y0 = int(bg.height * foco_y - H / 2); y0 = max(0, min(y0, bg.height - H))
    im = bg.crop(((bg.width - W) // 2, y0, (bg.width - W) // 2 + W, y0 + H))
    sombra = Image.new('RGBA', (W, H), (12, 3, 22, escurecer)); im.alpha_composite(sombra)
    lin = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lin)
    for y in range(0, H, 4): ld.line([(0, y), (W, y)], fill=(0, 0, 0, 20))
    im.alpha_composite(lin); return im

def topo(im, n, total):
    d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(RAIZ, 'logo', 'plaquinha-gta-loucura.png'))
    lw = 250; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    im.alpha_composite(logo, (48, 48))
    d.rectangle([330, 118, 900, 123], fill=CYAN)
    t = f'{n}/{total}'; f = fonte(40, 'Black')
    x1 = 1032; x0 = x1 - d.textlength(t, font=f) - 50
    d.polygon([(x0 + 14, 92), (x1, 92), (x1 - 14, 150), (x0, 150)], fill=PINK)
    d.text(((x0 + x1) / 2, 121), t, font=f, fill=DARK, anchor='mm')

def etiqueta(im, y, txt):
    d = ImageDraw.Draw(im); f = fonte(32, 'ExtraBold'); tw = d.textlength(txt, font=f)
    d.polygon([(64, y), (64 + tw + 70, y), (50 + tw + 70, y + 56), (50, y + 56)], fill=PINK)
    d.text((90, y + 28), txt, font=f, fill=DARK, anchor='lm')

def titulo(im, y, l1, l2, tam=96):
    d = ImageDraw.Draw(im)
    for i, (txt, cor) in enumerate([(l1, WHITE), (l2, PINK)]):
        if not txt: continue
        f = caber(d, txt, 'Black', tam, 960)
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(c)
        cd.text((56, y + 6), txt, font=f, fill=(8, 0, 16, 255), anchor='la')
        im.alpha_composite(c)
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(c).text((50, y), txt, font=f, fill=(*cor, 255), anchor='la')
        brilho(im, c, 14, 1) if cor == PINK else im.alpha_composite(c)
        y += f.size + 14
    return y

def paragrafo(im, y, txt, tam=40, cor=WHITE):
    d = ImageDraw.Draw(im); f = fonte(tam, 'SemiBold', it=False)
    for l in quebrar(d, txt, f, 960):
        d.text((54, y), l, font=f, fill=cor); y += int(tam * 1.32)
    return y

def faixa(im, y, txt):
    d = ImageDraw.Draw(im); bw = 980; sk = 26
    d.polygon([(64 + sk, y + 14), (64 + bw, y + 14), (64 + bw - sk, y + 118), (64, y + 118)], fill=CYAN)
    d.polygon([(50 + sk, y), (50 + bw, y), (50 + bw - sk, y + 104), (50, y + 104)], fill=PINK)
    d.text((50 + bw / 2, y + 52), txt, font=caber(d, txt, 'Black', 54, 900), fill=DARK, anchor='mm')

def fontes(im, txt):
    d = ImageDraw.Draw(im); d.rectangle([50, 1228, 1030, 1231], fill=CYAN)
    d.text((54, 1250), txt, font=fonte(26, 'SemiBold'), fill=(225, 215, 240))
    d.text((1030, 1250), '@gta6_loucura', font=fonte(28, 'Bold'), fill=PINK, anchor='ra')

def cartao_numero(im, y, numero, rotulo):
    d = ImageDraw.Draw(im)
    box = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
    bd.rounded_rectangle([50, y, 1030, y + 330], radius=34, fill=(14, 4, 28, 215), outline=(*CYAN, 255), width=5)
    brilho(im, box, 18, 1); d = ImageDraw.Draw(im)
    f = caber(d, numero, 'Black', 190, 900)
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(c).text((540, y + 140), numero, font=f, fill=(*GOLD, 255), anchor='mm')
    brilho(im, c, 20, 1)
    d.text((540, y + 270), rotulo, font=caber(d, rotulo, 'ExtraBold', 40, 880, it=False), fill=WHITE, anchor='mm')

def slide(s, n, total):
    im = fundo(s.get('foco', 0.55)); topo(im, n, total)
    if s.get('etiqueta'): etiqueta(im, 210, s['etiqueta'])
    y = titulo(im, 300, s.get('titulo_1', ''), s.get('titulo_2', ''), s.get('tam_titulo', 96)) + 30
    if s['tipo'] == 'numero':
        cartao_numero(im, y + 10, s['numero'], s['rotulo']); y += 380
    if s.get('texto'): y = paragrafo(im, y + 20, s['texto'])
    if s.get('faixa'): faixa(im, 1080, s['faixa'])
    fontes(im, s.get('fonte', ''))
    return im.convert('RGB')

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    for i, s in enumerate(spec, 1):
        slide(s, i, len(spec)).save(os.path.join(out, f'slide-{i:02d}.jpg'), quality=93)
    print('ok', len(spec))
