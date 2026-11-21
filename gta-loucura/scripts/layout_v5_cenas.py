"""Layout v5 da GTA Loucura: corte vertical (9:16) + texto de cena que muda a cada trecho.

Uso: python3 layout_v5_cenas.py roteiro.json pasta_saida
roteiro.json: {"etiqueta","titulo_1","titulo_2","cenas":[{"credito","linha_1","linha_2"}]}
Gera: moldura.png (janela transparente), previa.png e, por cena i,
cena{i}-a.png (só linha 1) e cena{i}-b.png (linhas 1 e 2) + credito{i}.png.
Regras: nada sobre a janela; textos abaixo da janela, à esquerda dos botões do Instagram.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout_v4_vertical as v4
from layout_v3 import fonte, caber, W, H, PINK, CYAN, WHITE

# janela menor para abrir espaço ao texto de cena
v4.VX0, v4.VY0, v4.VX1, v4.VY1 = 260, 420, 820, 1416
TY0, TY1 = 1450, 1570          # caixa do texto de cena
v4.SELO_Y = 1588               # selo AO VIVO e crédito abaixo da caixa

def caixa_cena(l1, l2=None):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([40, TY0, 960, TY1], radius=18, fill=(8, 2, 18, 215))
    im.alpha_composite(sh)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, TY0, 960, TY1], radius=18, outline=(*PINK, 230), width=3)
    d.rectangle([40, TY0 + 14, 48, TY1 - 14], fill=CYAN)
    f1 = caber(d, l1, 'ExtraBold', 40, 26, 860)
    d.text((70, TY0 + 34), l1, font=f1, fill=WHITE, anchor='lm')
    if l2:
        f2 = caber(d, l2, 'Black', 44, 26, 860)
        d.text((70, TY0 + 86), l2, font=f2, fill=(255, 214, 64), anchor='lm')
    return im

if __name__ == '__main__':
    r = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    t = {k: r[k] for k in ('etiqueta', 'titulo_1', 'titulo_2')}
    v4.montar(t, True).save(os.path.join(out, 'moldura.png'))
    for i, c in enumerate(r['cenas'], 1):
        caixa_cena(c['linha_1']).save(os.path.join(out, f'cena{i}-a.png'))
        caixa_cena(c['linha_1'], c['linha_2']).save(os.path.join(out, f'cena{i}-b.png'))
        v4.credito_png(c['credito'], os.path.join(out, f'credito{i}.png'))
    p = v4.montar(t); p.alpha_composite(Image.open(os.path.join(out, 'cena1-b.png'))); p.alpha_composite(Image.open(os.path.join(out, 'credito1.png')))
    p.convert('RGB').save(os.path.join(out, 'previa.png'))
    print('ok', len(r['cenas']))
