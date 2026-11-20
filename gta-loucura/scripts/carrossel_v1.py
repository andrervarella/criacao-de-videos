"""Carrossel GTA Loucura (1080x1350, 4:5) a partir de um JSON de slides.

Uso: python3 carrossel_v1.py slides.json pasta_saida [tema.json]
Sem tema = padrão GTA Loucura. Tema da marca André Varela: andre-varela/tema-av.json
Cada slide: {"tipo": "capa"|"numero"|"texto"|"cta", ...}. Veja um exemplo em
videos/2026-11-20-carrossel-bilhoes/slides.json.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.join(AQUI, '..')
W, H = 1080, 1350
PINK = (255, 36, 145); CYAN = (45, 230, 240); WHITE = (255, 255, 255); DARK = (22, 6, 36); GOLD = (255, 205, 80)
TEMA = {'logo': 'logo/plaquinha-gta-loucura.png', 'fundo': 'fundos/fundo-vice-neon-v1.png', 'handle': '@gta6_loucura', 'marca': None, 'submarca': None}
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
    if not TEMA.get('fundo'):
        im = Image.new('RGBA', (W, H), (8, 8, 10, 255)); d = ImageDraw.Draw(im)
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.ellipse([W - 420, -380, W + 380, 380], fill=(*PINK, 45))
        gd.ellipse([-300, H - 260, 380, H + 300], fill=(*PINK, 22))
        im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120)))
        lin = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lin)
        for x in range(-H, W, 46): ld.line([(x, H), (x + H, 0)], fill=(255, 255, 255, 3), width=2)
        im.alpha_composite(lin)
        return im
    bg = Image.open(os.path.join(RAIZ, TEMA['fundo'])).convert('RGBA')
    s = W / bg.width * 1.15; bg = bg.resize((int(bg.width * s), int(bg.height * s)), Image.LANCZOS)
    y0 = int(bg.height * foco_y - H / 2); y0 = max(0, min(y0, bg.height - H))
    im = bg.crop(((bg.width - W) // 2, y0, (bg.width - W) // 2 + W, y0 + H))
    sombra = Image.new('RGBA', (W, H), (12, 3, 22, escurecer)); im.alpha_composite(sombra)
    lin = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lin)
    for y in range(0, H, 4): ld.line([(0, y), (W, y)], fill=(0, 0, 0, 20))
    im.alpha_composite(lin); return im

def topo(im, n, total):
    d = ImageDraw.Draw(im)
    if TEMA.get('logo') and os.path.exists(os.path.join(RAIZ, TEMA['logo'])):
        logo = Image.open(os.path.join(RAIZ, TEMA['logo'])).convert('RGBA')
        lw = 250; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
        im.alpha_composite(logo, (48, 48))
    else:  # marca em texto (ex.: ANDRÉ VARELA / PERFORMANCE & EVOLUÇÃO)
        d.text((52, 70), TEMA.get('marca') or '', font=fonte(40, 'Black', it=False), fill=WHITE)
        d.text((54, 122), TEMA.get('submarca') or '', font=fonte(24, 'Bold', it=False), fill=PINK)
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
    f = fonte(26, 'SemiBold')
    while txt and d.textlength(txt, font=f) > 600: txt = txt[:-2].rstrip() + '…'
    d.text((54, 1250), txt, font=f, fill=(225, 215, 240))
    d.text((1030, 1250), TEMA['handle'], font=fonte(28, 'Bold'), fill=PINK, anchor='ra')

def cartao_numero(im, y, numero, rotulo):
    d = ImageDraw.Draw(im)
    box = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
    bd.rounded_rectangle([50, y, 1030, y + 330], radius=34, fill=(14, 4, 28, 215) if TEMA.get('fundo') else (18, 18, 22, 230), outline=(*CYAN, 255), width=5)
    brilho(im, box, 18, 1); d = ImageDraw.Draw(im)
    f = caber(d, numero, 'Black', 190, 900)
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(c).text((540, y + 140), numero, font=f, fill=(*GOLD, 255), anchor='mm')
    brilho(im, c, 20, 1)
    d.text((540, y + 270), rotulo, font=caber(d, rotulo, 'ExtraBold', 40, 880, it=False), fill=WHITE, anchor='mm')

def foto(im, y, h, caminho, credito):
    """Foto em cartão com borda neon e crédito visível no canto."""
    d = ImageDraw.Draw(im)
    src = Image.open(caminho).convert('RGBA'); bw = 980
    r = max(bw / src.width, h / src.height)
    src = src.resize((int(src.width * r), int(src.height * r)), Image.LANCZOS)
    src = src.crop(((src.width - bw) // 2, (src.height - h) // 2, (src.width - bw) // 2 + bw, (src.height - h) // 2 + h))
    m = Image.new('L', (bw, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw, h], radius=30, fill=255)
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(fr).rounded_rectangle([44, y - 6, 1036, y + h + 6], radius=36, outline=(*CYAN, 255), width=6)
    brilho(im, fr, 18, 1)
    im.paste(src, (50, y), m)
    d = ImageDraw.Draw(im); f = fonte(22, 'Bold', it=False); tw = d.textlength(credito, font=f)
    d.rounded_rectangle([1030 - tw - 28, y + h - 44, 1022, y + h - 10], radius=10, fill=(10, 4, 24, 220))
    d.text((1030 - 14 - tw, y + h - 27), credito, font=f, fill=(235, 225, 245), anchor='lm')

def slide(s, n, total):
    im = fundo(s.get('foco', 0.55)); topo(im, n, total)
    if s.get('foto_topo'):
        ft = s['foto_topo']; foto(im, 240, ft.get('h', 360), ft['arquivo'], ft['credito'])
        im2 = ImageDraw.Draw(im)
    base = (240 + s['foto_topo'].get('h', 360) + 30) if s.get('foto_topo') else 210
    if s.get('etiqueta'): etiqueta(im, base, s['etiqueta'])
    y = titulo(im, base + 90, s.get('titulo_1', ''), s.get('titulo_2', ''), s.get('tam_titulo', 96)) + 30
    if s['tipo'] == 'numero':
        cartao_numero(im, y + 10, s['numero'], s['rotulo']); y += 380
    if s.get('texto'): y = paragrafo(im, y + 20, s['texto'])
    if s.get('faixa'): faixa(im, 1100 if s.get('foto_topo') else 1080, s['faixa'])
    fontes(im, s.get('fonte', ''))
    return im.convert('RGB')

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    if len(sys.argv) > 3:
        t = json.load(open(sys.argv[3], encoding='utf-8'))
        RAIZ = os.path.dirname(os.path.abspath(sys.argv[3]))
        TEMA.update(t.get('tema', {}))
        PINK = tuple(t['cores']['destaque']); CYAN = tuple(t['cores']['linha']); GOLD = tuple(t['cores']['numero']); DARK = tuple(t['cores']['texto_faixa'])
    for i, s in enumerate(spec, 1):
        slide(s, i, len(spec)).save(os.path.join(out, f'slide-{i:02d}.jpg'), quality=93)
    print('ok', len(spec))
