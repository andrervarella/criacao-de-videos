"""Layout v4 da GTA Loucura (Reels 1080x1920) para cortes VERTICAIS (câmera + gameplay empilhados).

Uso:  python3 layout_v4_vertical.py textos.json saida.png
Gera saida.png (prévia) e saida-moldura.png (janela 9:16 transparente).
Regras fixas: nada sobre a janela; selo AO VIVO e crédito ABAIXO dela, à esquerda;
janela termina antes da coluna de botões do Instagram (x < 900).
O crédito de cada trecho é gerado à parte (credito_png) para trocar por cena.
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v3 import fundo, fonte, caber, brilho, estrela, RAIZ, W, H, PINK, CYAN, WHITE, DARK, RED

VX0, VY0, VX1, VY1 = 230, 440, 850, 1542   # janela 9:16 (620 x 1102)

def montar(t, janela_transparente=False):
    im = fundo(); d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(RAIZ, 'logo', 'plaquinha-gta-loucura.png'))
    lw = 250; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((255, 36, 145, 255), (40, 58), logo)
    sh = sh.filter(__import__('PIL.ImageFilter', fromlist=['x']).GaussianBlur(20)); im.alpha_composite(sh)
    im.alpha_composite(logo, (40, 52))
    hud = Image.new('RGBA', (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(hud)
    for i in range(5):
        estrela(hd, 760 + i * 58, 92, 22, (*WHITE, 255) if i < 4 else (*WHITE, 70))
    brilho(im, hud, 8, 1); d = ImageDraw.Draw(im)
    def para(x, y, w, h, fill, sk=14):
        d.polygon([(x + sk, y), (x + w, y), (x + w - sk, y + h), (x, y + h)], fill=fill)
    ft = fonte(28, 'ExtraBold'); tw = d.textlength(t['etiqueta'], font=ft)
    para(700 - 0 if False else 1040 - tw - 70, 140, tw + 70, 48, PINK)
    d.text((1040 - tw - 32, 164), t['etiqueta'], font=ft, fill=DARK, anchor='lm')
    def texto_sombra(xy, txt, font, fill, glow=None):
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(c).text((xy[0] + 5, xy[1] + 5), txt, font=font, fill=(10, 0, 20, 255), anchor='mm')
        im.alpha_composite(c)
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(c).text(xy, txt, font=font, fill=fill, anchor='mm')
        brilho(im, c, glow, 1) if glow else im.alpha_composite(c)
    texto_sombra((W / 2, 268), t['titulo_1'], caber(d, t['titulo_1'], 'Black', 78, 40, 1000), (*WHITE, 255))
    texto_sombra((W / 2, 366), t['titulo_2'], caber(d, t['titulo_2'], 'Black', 104, 40, 1000), (*PINK, 255), glow=16)
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(fr).rounded_rectangle([VX0 - 6, VY0 - 6, VX1 + 6, VY1 + 6], radius=30, outline=(*CYAN, 255), width=6)
    brilho(im, fr, 22, 2); d = ImageDraw.Draw(im)
    if janela_transparente:
        mask = Image.new('L', (W, H), 255)
        ImageDraw.Draw(mask).rounded_rectangle([VX0, VY0, VX1, VY1], radius=26, fill=0)
        im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')), np.array(mask))))
        d = ImageDraw.Draw(im)
    else:
        d.rounded_rectangle([VX0, VY0, VX1, VY1], radius=26, fill=(12, 10, 22, 235))
        d.text(((VX0 + VX1) / 2, (VY0 + VY1) / 2), 'CORTE 9:16', font=fonte(34, 'Bold'), fill=(255, 255, 255, 120), anchor='mm')
    for (x, y, sx, sy) in [(VX0 - 20, VY0 - 20, 1, 1), (VX1 + 20, VY0 - 20, -1, 1), (VX0 - 20, VY1 + 20, 1, -1), (VX1 + 20, VY1 + 20, -1, -1)]:
        d.line([(x, y), (x + sx * 54, y)], fill=PINK, width=8); d.line([(x, y), (x, y + sy * 54)], fill=PINK, width=8)
    # selo AO VIVO abaixo da janela, à esquerda
    bx0, by0 = 60, VY1 + 38
    d.rounded_rectangle([bx0, by0, bx0 + 176, by0 + 46], radius=10, fill=RED)
    d.ellipse([bx0 + 16, by0 + 15, bx0 + 32, by0 + 31], fill=WHITE)
    d.text((bx0 + 42, by0 + 23), 'AO VIVO', font=fonte(28, 'Black'), fill=WHITE, anchor='lm')
    return im

def credito_png(texto, saida):
    """Pílula de crédito (ao lado do selo AO VIVO), trocada a cada trecho."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ft = fonte(26, 'SemiBold', italic=False); tw = d.textlength(texto, font=ft)
    x0, y0 = 256, VY1 + 38
    d.rounded_rectangle([x0, y0, x0 + tw + 40, y0 + 46], radius=23, fill=(10, 4, 24, 225), outline=(*CYAN, 200), width=2)
    d.text((x0 + 20, y0 + 23), texto, font=ft, fill=(225, 215, 240), anchor='lm')
    im.save(saida)

if __name__ == '__main__':
    t = {"etiqueta": "GTA 6 • AO VIVO", "titulo_1": "TÍTULO 1", "titulo_2": "TÍTULO 2"}
    if len(sys.argv) > 1: t.update(json.load(open(sys.argv[1], encoding='utf-8')))
    out = sys.argv[2] if len(sys.argv) > 2 else 'layout_v4.png'
    montar(t).convert('RGB').save(out)
    montar(t, True).save(out.replace('.png', '-moldura.png'))
    for i, c in enumerate(t.get('creditos', [])):
        credito_png(c, out.replace('.png', f'-credito{i + 1}.png'))
    print('ok', out)
