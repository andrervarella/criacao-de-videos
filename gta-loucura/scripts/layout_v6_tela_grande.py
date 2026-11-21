"""Layout v6 da GTA Loucura: vídeo GRANDE (9:16, 800x1422) e faixa de texto no topo que muda por cena.

Uso: python3 layout_v6_tela_grande.py roteiro.json pasta_saida
roteiro.json: {"textos":[{"id","linha_1","linha_2"}], "creditos":[{"id","texto"}], "final":[linhas]}
Gera: base.png (moldura com janela transparente), faixa-<id>.png, credito-<id>.png, final.png.
Regras: nada sobre a janela; textos no topo (fora dos botões e da legenda do Instagram);
selo AO VIVO e crédito na linha de cima, fora da janela.
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v3 import fonte, caber, brilho, RAIZ, W, H, PINK, CYAN, WHITE, DARK, RED

VX0, VY0, VX1, VY1 = 140, 360, 940, 1782     # janela 9:16 (800 x 1422)
FUNDO = None   # caminho de outra imagem de fundo (preenche a tela); padrão: fundo-vice-neon-v1
ESCURECER = 150
AMARELO = (255, 214, 64)

def base(janela_transparente=True):
    im = Image.new('RGBA', (W, H), (12, 4, 26, 255))
    if FUNDO:
        bg = Image.open(FUNDO).convert('RGBA'); r = max(W / bg.width, H / bg.height)
        bg = bg.resize((int(bg.width * r) + 1, int(bg.height * r) + 1), Image.LANCZOS)
        x0 = (bg.width - W) // 2; y0 = (bg.height - H) // 2
        im.alpha_composite(bg.crop((x0, y0, x0 + W, y0 + H)))
    else:
        bg = Image.open(os.path.join(RAIZ, 'fundos', 'fundo-vice-neon-v1.png')).convert('RGBA')
        bg = bg.resize((W, int(bg.height * W / bg.width)), Image.LANCZOS)
        im.alpha_composite(bg, (0, H - bg.height))
    esc = Image.new('RGBA', (W, H), (8, 2, 18, ESCURECER)); im.alpha_composite(esc)
    d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(RAIZ, 'logo', 'plaquinha-gta-loucura.png'))
    lw = 150; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    im.alpha_composite(logo, (36, 26))
    bx0, by0 = 206, 40
    d.rounded_rectangle([bx0, by0, bx0 + 150, by0 + 40], radius=9, fill=RED)
    d.ellipse([bx0 + 14, by0 + 13, bx0 + 28, by0 + 27], fill=WHITE)
    d.text((bx0 + 38, by0 + 20), 'AO VIVO', font=fonte(24, 'Black'), fill=WHITE, anchor='lm')
    d.rounded_rectangle([372, 58, 640, 62], radius=2, fill=CYAN)
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(fr).rounded_rectangle([VX0 - 5, VY0 - 5, VX1 + 5, VY1 + 5], radius=26, outline=(*CYAN, 255), width=5)
    brilho(im, fr, 16, 1)
    if janela_transparente:
        mask = Image.new('L', (W, H), 255)
        ImageDraw.Draw(mask).rounded_rectangle([VX0, VY0, VX1, VY1], radius=22, fill=0)
        im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')), np.array(mask))))
    return im

def faixa(l1, l2):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def txt(y, t, f, cor, glow=None):
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(c)
        cd.text((W / 2 + 4, y + 4), t, font=f, fill=(10, 0, 20, 255), anchor='mm', stroke_width=3, stroke_fill=(10, 0, 20, 255))
        cd.text((W / 2, y), t, font=f, fill=(*cor, 255), anchor='mm', stroke_width=3, stroke_fill=(10, 0, 20, 255))
        brilho(im, c, glow, 1) if glow else im.alpha_composite(c)
    if l1: txt(150, l1, caber(d, l1, 'ExtraBold', 50, 28, 1010), WHITE)
    if l2: txt(240, l2, caber(d, l2, 'Black', 78, 36, 1010), AMARELO, glow=10)
    return im

INTER = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
INTER_IT = '/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf'

def _f(path, s):
    from PIL import ImageFont
    return ImageFont.truetype(path, s)

def _caber(d, t, path, smax, smin, larg):
    s = smax
    while s > smin and d.textlength(t, font=_f(path, s)) > larg: s -= 2
    return _f(path, s)

def faixa_carrossel(l1, l2, destaque=False):
    """Estilo das letras dos carrosséis: linha 1 branca pesada; linha 2 em faixa rosa inclinada
    com barra ciano (ou, em destaque, texto rosa gigante)."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def sombra_txt(xy, t, f, cor, anchor='mm', glow=None):
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(c)
        cd.text((xy[0] + 4, xy[1] + 5), t, font=f, fill=(10, 0, 20, 230), anchor=anchor)
        im.alpha_composite(c.filter(ImageFilter.GaussianBlur(3)))
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(c).text(xy, t, font=f, fill=(*cor, 255), anchor=anchor)
        brilho(im, c, glow, 1) if glow else im.alpha_composite(c)
    if l1: sombra_txt((W / 2, 170), l1, _caber(d, l1, INTER, 64, 30, 1000), WHITE)
    if l2 and destaque:
        sombra_txt((W / 2, 272), l2, _caber(d, l2, INTER_IT, 118, 40, 1000), PINK, glow=12)
    elif l2:
        f = _caber(d, l2, INTER_IT, 52, 28, 880); tw = d.textlength(l2, font=f)
        x0 = (W - tw) / 2 - 30; x1 = (W + tw) / 2 + 30; y0, y1 = 226, 310; sk = 22
        d.polygon([(x0 + sk, y0), (x1 + sk, y0), (x1 - sk, y1), (x0 - sk, y1)], fill=PINK)
        d.polygon([(x0 - sk - 34, y0), (x0 - sk - 22, y0), (x0 - sk - 42, y1), (x0 - sk - 54, y1)], fill=CYAN)
        d.text(((x0 + x1) / 2, (y0 + y1) / 2 + 2), l2, font=f, fill=WHITE, anchor='mm')
    return im

def credito(t):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ft = fonte(22, 'SemiBold', italic=False); tw = d.textlength(t, font=ft)
    x1 = 1044; x0 = x1 - tw - 36
    d.rounded_rectangle([x0, 40, x1, 80], radius=20, fill=(10, 4, 24, 225), outline=(*CYAN, 200), width=2)
    d.text((x0 + 18, 60), t, font=ft, fill=(225, 215, 240), anchor='lm')
    return im

def final(linhas):
    im = base(False).convert('RGBA'); d = ImageDraw.Draw(im)
    d.rounded_rectangle([VX0, VY0, VX1, VY1], radius=22, fill=(10, 4, 24, 255))
    logo = Image.open(os.path.join(RAIZ, 'logo', 'plaquinha-gta-loucura.png')); lw = 520
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    im.alpha_composite(logo, ((W - lw) // 2, 470))
    y = 900
    for t, s, cor in linhas:
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(c).text((W / 2, y), t, font=caber(d, t, 'Black', s, 30, 760), fill=(*cor, 255), anchor='mm')
        brilho(im, c, 10, 1); y += int(s * 1.45)
    return im

if __name__ == '__main__':
    r = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    if r.get('fundo'): FUNDO = r['fundo']
    if r.get('escurecer') is not None: ESCURECER = r['escurecer']
    base().save(os.path.join(out, 'base.png'))
    estilo = r.get('estilo_letras', 'v6')
    def _faixa(f):
        if estilo == 'carrossel': return faixa_carrossel(f['linha_1'], f.get('linha_2'), f.get('destaque', False))
        return faixa(f['linha_1'], f.get('linha_2'))
    for f in r['textos']: _faixa(f).save(os.path.join(out, f"faixa-{f['id']}.png"))
    for c in r['creditos']: credito(c['texto']).save(os.path.join(out, f"credito-{c['id']}.png"))
    cores = {'branco': WHITE, 'rosa': PINK, 'ciano': CYAN, 'amarelo': AMARELO}
    final([(t, s, cores[c]) for t, s, c in r['final']]).convert('RGB').save(os.path.join(out, 'final.png'))
    p = base(False); f0 = r['textos'][0]
    p.alpha_composite(_faixa(f0)); p.alpha_composite(credito(r['creditos'][0]['texto']))
    p.convert('RGB').save(os.path.join(out, 'previa.png'))
    print('ok')
