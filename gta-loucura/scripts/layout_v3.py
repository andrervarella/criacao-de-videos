"""Layout v3 da GTA Loucura (Reels 1080x1920) com o fundo neon de Vice City.

Uso:  python3 layout_v3.py textos.json saida.png
Os textos mudam a cada vídeo (veja TEXTOS_PADRAO). A janela do vídeo (16:9)
fica transparente na versão "moldura", para a montagem no vidIQ.
"""
import json, math, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, '..')
W, H = 1080, 1920
PINK = (255, 36, 145); CYAN = (45, 230, 240); WHITE = (255, 255, 255)
DARK = (22, 6, 36); RED = (255, 59, 59)
MI = '/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat-Italic[wght].ttf'
MR = '/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf'
VX0, VY0, VX1, VY1 = 40, 700, 1040, 1262   # janela do vídeo 16:9

TEXTOS_PADRAO = {
    "etiqueta": "CORTE DE LIVE  •  STREAMER",
    "titulo_1": "TÍTULO LINHA 1",
    "titulo_2": "TÍTULO LINHA 2!",
    "legenda_1": "Primeira linha explicando o que acontece…",
    "legenda_2": "segunda linha com o desfecho.",
    "faixa": "FRASE DE IMPACTO AQUI",
    "credito": "FONTE: CANAL DO STREAMER • DATA",
    "contador": "CORTE DO DIA #001",
}

def fonte(size, w='Black', italic=True):
    ft = ImageFont.truetype(MI if italic else MR, size)
    ft.set_variation_by_name(f'{w} Italic' if italic else w)
    return ft

def caber(d, texto, w, size_max, size_min=40, largura=1000):
    s = size_max
    while s > size_min and d.textlength(texto, font=fonte(s, w)) > largura:
        s -= 2
    return fonte(s, w)

def brilho(base, camada, raio=18, vezes=2):
    g = camada.filter(ImageFilter.GaussianBlur(raio))
    for _ in range(vezes):
        base.alpha_composite(g)
    base.alpha_composite(camada)

def fundo():
    bg = Image.open(os.path.join(RAIZ, 'fundos', 'fundo-vice-neon-v1.png')).convert('RGBA')
    s = 1.18                                   # zoom: cidade e sol descem para baixo do vídeo
    bg = bg.resize((int(bg.width * W / bg.width * s), int(bg.height * W / bg.width * s)), Image.LANCZOS)
    tela = Image.new('RGBA', (W, H), bg.getpixel((bg.width // 2, 5)))
    tela.alpha_composite(bg, ((W - bg.width) // 2, 150))
    # escurece topo (logo/título) e base (área do Instagram)
    sombra = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sombra)
    for y in range(H):
        a = 0
        if y < 680: a = int(150 * (1 - y / 680) + 40)
        if y > 1500: a = max(a, int(170 * (y - 1500) / 420))
        sd.line([(0, y), (W, y)], fill=(10, 2, 20, a))
    tela.alpha_composite(sombra)
    lin = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lin)
    for y in range(0, H, 4):
        ld.line([(0, y), (W, y)], fill=(0, 0, 0, 22))
    tela.alpha_composite(lin)
    return tela

def estrela(dr, cx, cy, R, fill):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; r = R if i % 2 == 0 else R * 0.45
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    dr.polygon(pts, fill=fill)

def montar(t, janela_transparente=False):
    im = fundo(); d = ImageDraw.Draw(im)
    # logo com brilho rosa
    logo = Image.open(os.path.join(RAIZ, 'logo', 'plaquinha-gta-loucura.png'))
    lw = 330; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((255, 36, 145, 255), (40, 128), logo)
    sh = sh.filter(ImageFilter.GaussianBlur(22)); im.alpha_composite(sh); im.alpha_composite(sh)
    im.alpha_composite(logo, (40, 120))
    # estrelas de procurado + contador
    hud = Image.new('RGBA', (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(hud)
    for i in range(5):
        estrela(hd, 690 + i * 62, 190, 24, (*WHITE, 255) if i < 4 else (*WHITE, 70))
    brilho(im, hud, 8, 1)
    ft = fonte(30, 'ExtraBold'); tw = d.textlength(t['contador'], font=ft); x1 = 1040; x0 = x1 - tw - 44
    d.rounded_rectangle([x0, 232, x1, 282], radius=25, outline=CYAN, width=3, fill=(10, 4, 24, 210))
    d.text(((x0 + x1) / 2, 257), t['contador'], font=ft, fill=CYAN, anchor='mm')
    # etiqueta
    def para(x, y, w, h, fill, sk=16):
        d.polygon([(x + sk, y), (x + w, y), (x + w - sk, y + h), (x, y + h)], fill=fill)
    ft = fonte(32, 'ExtraBold'); tw = d.textlength(t['etiqueta'], font=ft)
    para(40, 380, tw + 110, 56, PINK)
    d.polygon([(68, 396), (68, 420), (88, 408)], fill=DARK)
    d.text((102, 408), t['etiqueta'], font=ft, fill=DARK, anchor='lm')
    # título (tamanho se ajusta ao texto)
    def texto_sombra(xy, txt, font, fill, glow=None):
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(c).text((xy[0] + 6, xy[1] + 6), txt, font=font, fill=(10, 0, 20, 255), anchor='lm')
        im.alpha_composite(c)
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(c).text(xy, txt, font=font, fill=fill, anchor='lm')
        brilho(im, c, glow, 1) if glow else im.alpha_composite(c)
    texto_sombra((40, 506), t['titulo_1'], caber(d, t['titulo_1'], 'Black', 84), (*WHITE, 255))
    texto_sombra((40, 612), t['titulo_2'], caber(d, t['titulo_2'], 'Black', 118), (*PINK, 255), glow=16)
    # janela do vídeo
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(fr).rounded_rectangle([VX0 - 6, VY0 - 6, VX1 + 6, VY1 + 6], radius=34, outline=(*CYAN, 255), width=6)
    brilho(im, fr, 22, 2); d = ImageDraw.Draw(im)
    if janela_transparente:
        mask = Image.new('L', (W, H), 255)
        ImageDraw.Draw(mask).rounded_rectangle([VX0, VY0, VX1, VY1], radius=28, fill=0)
        im.putalpha(Image.fromarray(__import__('numpy').minimum(__import__('numpy').array(im.getchannel('A')), __import__('numpy').array(mask))))
        d = ImageDraw.Draw(im)
    else:
        d.rounded_rectangle([VX0, VY0, VX1, VY1], radius=28, fill=(12, 10, 22, 235))
        cx, cy = (VX0 + VX1) // 2, (VY0 + VY1) // 2
        d.ellipse([cx - 60, cy - 90, cx + 60, cy + 30], outline=(255, 255, 255, 120), width=5)
        d.polygon([(cx - 18, cy - 58), (cx - 18, cy - 2), (cx + 30, cy - 30)], fill=(255, 255, 255, 140))
        d.text((cx, cy + 80), 'SEU CORTE AQUI  •  16:9', font=fonte(34, 'Bold'), fill=(255, 255, 255, 120), anchor='mm')
    for (x, y, sx, sy) in [(VX0 - 22, VY0 - 22, 1, 1), (VX1 + 22, VY0 - 22, -1, 1), (VX0 - 22, VY1 + 22, 1, -1), (VX1 + 22, VY1 + 22, -1, -1)]:
        d.line([(x, y), (x + sx * 60, y)], fill=PINK, width=8); d.line([(x, y), (x, y + sy * 60)], fill=PINK, width=8)
    d.rounded_rectangle([VX0 + 24, VY0 + 24, VX0 + 190, VY0 + 72], radius=10, fill=RED)
    d.ellipse([VX0 + 40, VY0 + 40, VX0 + 56, VY0 + 56], fill=WHITE)
    d.text((VX0 + 66, VY0 + 48), 'AO VIVO', font=fonte(28, 'Black'), fill=WHITE, anchor='lm')
    # legenda com faixa escura
    band = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(band).rectangle([0, 1290, W, 1425], fill=(14, 4, 28, 200))
    im.alpha_composite(band.filter(ImageFilter.GaussianBlur(14))); d = ImageDraw.Draw(im)
    fb = fonte(40, 'Bold', italic=False)
    d.text((44, 1312), t['legenda_1'], font=fb, fill=WHITE)
    d.text((44, 1362), t['legenda_2'], font=fb, fill=(255, 190, 225))
    # faixa rosa com sombra ciano (fora da área dos botões do Instagram)
    y, bw = 1450, 890
    para(54, y + 14, bw, 104, CYAN, 24); para(40, y, bw, 104, PINK, 24)
    d.text((40 + bw / 2, y + 52), t['faixa'], font=caber(d, t['faixa'], 'Black', 50, 32, 820), fill=DARK, anchor='mm')
    # crédito
    ft = fonte(26, 'SemiBold', italic=False); tw = d.textlength(t['credito'], font=ft)
    d.rounded_rectangle([40, 1590, 40 + tw + 40, 1636], radius=23, fill=(10, 4, 24, 220), outline=(*CYAN, 180), width=2)
    d.text((60, 1613), t['credito'], font=ft, fill=(225, 215, 240), anchor='lm')
    return im

if __name__ == '__main__':
    textos = dict(TEXTOS_PADRAO)
    if len(sys.argv) > 1 and sys.argv[1].endswith('.json'):
        textos.update(json.load(open(sys.argv[1], encoding='utf-8')))
    saida = sys.argv[2] if len(sys.argv) > 2 else 'layout_v3.png'
    montar(textos).convert('RGB').save(saida)
    montar(textos, janela_transparente=True).save(saida.replace('.png', '-moldura.png'))
    print('ok', saida)
