"""Carrossel André Varela (1080x1350, 4:5) — visual premium: preto, prata, vermelho #A11218 pontual.

Uso: python3 carrossel_av_v1.py slides.json pasta_saida
Tipos de slide: capa (foto de fundo), texto, numero, compara, lista, cta.
Campos comuns: etiqueta, titulo_1, titulo_2, texto, nota, fonte.
- capa: foto {arquivo, foco_x, foco_y, recorte:[x0,y0,x1,y1] opcional}
- numero: numero, rotulo
- compara: esq {topo, titulo, texto}, dir {topo, titulo, texto}
- lista: itens [str]
A logo é o arquivo oficial recortado (logo/logo-av.png), nunca redesenhada.
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.join(AQUI, '..')
W, H, M = 1080, 1350, 72
PRETO = (9, 9, 11); BRANCO = (245, 245, 247); PRATA = (176, 180, 188); CINZA = (128, 131, 138); VERM = (161, 18, 24)
MR = '/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf'
HANDLE = '@treinadorandrevarela'

def F(s, w='Bold'):
    f = ImageFont.truetype(MR, s); f.set_variation_by_name(w); return f

def espacado(d, xy, txt, f, fill, esp=0.18, anchor='l'):
    x, y = xy; larg = sum(d.textlength(c, font=f) for c in txt) + esp * f.size * (len(txt) - 1)
    if anchor == 'r': x -= larg
    for c in txt:
        d.text((x, y), c, font=f, fill=fill); x += d.textlength(c, font=f) + esp * f.size
    return larg

def quebrar(d, txt, f, larg):
    linhas, at = [], ''
    for p in txt.split():
        t = (at + ' ' + p).strip()
        if d.textlength(t, font=f) <= larg: at = t
        else: linhas.append(at); at = p
    return linhas + ([at] if at else [])

def caber(d, txt, w, smax, larg, smin=34):
    s = smax
    while s > smin and d.textlength(txt, font=F(s, w)) > larg: s -= 2
    return F(s, w)

def fundo():
    im = Image.new('RGBA', (W, H), PRETO + (255,))
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([-200, -500, W + 200, 500], fill=(60, 62, 70, 70))
    gd.ellipse([W - 330, H - 300, W + 330, H + 330], fill=VERM + (40,))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
    rng = np.random.default_rng(7); n = (rng.normal(0, 1, (H, W)) * 5).clip(-12, 12)
    a = np.asarray(im).astype(float); a[..., :3] = (a[..., :3] + n[..., None]).clip(0, 255)
    return Image.fromarray(a.astype('uint8'), 'RGBA')

def topo(im, n, total):
    d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(RAIZ, 'logo/logo-av.png')).convert('RGBA')
    lw = 112; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    im.alpha_composite(logo, (M, 62))
    espacado(d, (M + lw + 22, 64), 'ANDRÉ VARELA', F(26, 'SemiBold'), BRANCO, 0.22)
    espacado(d, (M + lw + 22, 100), 'PERFORMANCE & EVOLUÇÃO', F(15, 'Medium'), PRATA, 0.28)
    # Sem contador de páginas (1/7): o Instagram já mostra, e o André acha que deixa cara de IA.

def rodape(im, fonte):
    d = ImageDraw.Draw(im); d.rectangle([M, 1252, W - M, 1253], fill=(70, 72, 78))
    f = F(20, 'Medium'); txt = fonte or ''
    while txt and d.textlength(txt, font=f) > 640: txt = txt[:-2].rstrip() + '…'
    d.text((M, 1272), txt, font=f, fill=CINZA)
    d.text((W - M, 1272), HANDLE, font=F(20, 'SemiBold'), fill=PRATA, anchor='ra')

def etiqueta(im, y, txt):
    d = ImageDraw.Draw(im); f = F(20, 'Bold')
    larg = sum(d.textlength(c, font=f) for c in txt) + 0.2 * 20 * (len(txt) - 1)
    d.rounded_rectangle([M, y, M + larg + 40, y + 44], radius=6, fill=VERM)
    espacado(d, (M + 20, y + 10), txt, f, BRANCO, 0.2)
    return y + 44

def titulo(im, y, l1, l2, tam=84):
    d = ImageDraw.Draw(im)
    for txt, cor in [(l1, BRANCO), (l2, PRATA)]:
        if not txt: continue
        f = caber(d, txt, 'ExtraBold', tam, W - 2 * M)
        d.text((M - 3, y), txt, font=f, fill=cor); y += int(f.size * 1.12)
    return y

def paragrafo(im, y, txt, tam=36, cor=BRANCO, peso='Medium', larg=W - 2 * M, x=M):
    d = ImageDraw.Draw(im); f = F(tam, peso)
    for l in quebrar(d, txt, f, larg):
        d.text((x, y), l, font=f, fill=cor); y += int(tam * 1.38)
    return y

def painel(im, box, borda=(255, 255, 255, 38)):
    p = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(p).rounded_rectangle(box, radius=22, fill=(20, 20, 24, 225), outline=borda, width=2)
    im.alpha_composite(p)

def foto_capa(im, ft):
    src = Image.open(ft['arquivo']).convert('RGBA')
    if ft.get('recorte'): src = src.crop(tuple(ft['recorte']))
    r = max(W / src.width, H / src.height); src = src.resize((int(src.width * r) + 1, int(src.height * r) + 1), Image.LANCZOS)
    fx, fy = ft.get('foco_x', 0.5), ft.get('foco_y', 0.35)
    x0 = int(max(0, min(src.width - W, src.width * fx - W / 2))); y0 = int(max(0, min(src.height - H, src.height * fy - H / 2)))
    im.alpha_composite(src.crop((x0, y0, x0 + W, y0 + H)))
    g = np.zeros((H, W, 4), 'uint8'); ys = np.arange(H)
    a = np.clip((ys - 560) / 520, 0, 1) ** 1.2 * 250 + np.clip((260 - ys) / 260, 0, 1) * 170
    g[..., 3] = a.clip(0, 252)[:, None]; g[..., :3] = PRETO
    im.alpha_composite(Image.fromarray(g, 'RGBA'))

def slide(s, n, total, y_ini=None):
    im = fundo()
    if s['tipo'] == 'capa': foto_capa(im, s['foto'])
    topo(im, n, total); d = ImageDraw.Draw(im)
    y = 830 if s['tipo'] == 'capa' else (y_ini or 230)
    if s.get('etiqueta'): y = etiqueta(im, y, s['etiqueta']) + 34
    y = titulo(im, y, s.get('titulo_1', ''), s.get('titulo_2', ''), s.get('tam_titulo', 84)) + 26
    t = s['tipo']
    if t == 'numero':
        painel(im, [M, y, W - M, y + 400])
        f = caber(d, s['numero'], 'ExtraBold', 210, W - 2 * M - 80)
        d.text((W / 2, y + 160), s['numero'], font=f, fill=BRANCO, anchor='mm')
        d.rectangle([W / 2 - 50, y + 278, W / 2 + 50, y + 283], fill=VERM)
        yy = y + 312
        for l in quebrar(d, s['rotulo'], F(34, 'SemiBold'), W - 2 * M - 100):
            d.text((W / 2, yy), l, font=F(34, 'SemiBold'), fill=PRATA, anchor='ma'); yy += 44
        y += 440
    elif t == 'compara':
        cw = (W - 2 * M - 24) // 2
        for i, lado in enumerate([s['esq'], s['dir']]):
            x = M + i * (cw + 24); destaque = i == 1
            painel(im, [x, y, x + cw, y + 470], borda=VERM + (255,) if destaque else (255, 255, 255, 38))
            espacado(d, (x + 30, y + 34), lado['topo'], F(19, 'Bold'), VERM if destaque else CINZA, 0.18)
            f = caber(d, lado['titulo'], 'ExtraBold', 92, cw - 60)
            d.text((x + 30, y + 80), lado['titulo'], font=f, fill=BRANCO)
            paragrafo(im, y + 220, lado['texto'], 30, PRATA, 'Medium', cw - 60, x + 30)
        y += 510
    elif t == 'lista':
        for i, item in enumerate(s['itens'], 1):
            d.text((M, y), f'{i:02d}', font=F(40, 'ExtraBold'), fill=VERM)
            y2 = paragrafo(im, y + 2, item, 36, BRANCO, 'SemiBold', W - 2 * M - 90, M + 90)
            y = max(y2, y + 60) + 26
    def bloco_destaque(y):
        y += 20; d.rectangle([M, y + 6, M + 6, y + 6 + 46 * len(quebrar(d, s['destaque'], F(34, 'Bold'), W - 2 * M - 30))], fill=VERM)
        return paragrafo(im, y, s['destaque'], 34, BRANCO, 'Bold', W - 2 * M - 30, M + 30) + 20
    if t == 'cta' and s.get('destaque'): y = bloco_destaque(y) + 10
    if s.get('texto'): y = paragrafo(im, y + 6, s['texto'], s.get('tam_texto', 36), BRANCO if t not in ('capa', 'cta') else PRATA)
    if t != 'cta' and s.get('destaque'): y = bloco_destaque(y)
    if t == 'cta':  # assinatura com o monograma oficial
        logo = Image.open(os.path.join(RAIZ, 'logo/logo-av.png')).convert('RGBA')
        lw = 300; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
        y += 50; im.alpha_composite(logo, ((W - lw) // 2, y)); y += logo.height + 26
        lm = espacado(ImageDraw.Draw(Image.new('L', (1, 1))), (0, 0), 'ANDRÉ VARELA', F(34, 'SemiBold'), 0, 0.25)
        espacado(d, ((W - lm) / 2, y), 'ANDRÉ VARELA', F(34, 'SemiBold'), BRANCO, 0.25); y += 54
        larg = espacado(ImageDraw.Draw(Image.new('L', (1, 1))), (0, 0), 'PERFORMANCE & EVOLUÇÃO', F(18, 'Medium'), 0, 0.3)
        espacado(d, ((W - larg) / 2, y), 'PERFORMANCE & EVOLUÇÃO', F(18, 'Medium'), VERM, 0.3); y += 30
    if s.get('nota'): paragrafo(im, 1166 - 30 * (len(quebrar(d, s['nota'], F(22, 'Medium'), W - 2 * M)) - 1), s['nota'], 22, CINZA, 'Medium')
    rodape(im, s.get('fonte', ''))
    return im.convert('RGB'), y

def render(s, n, total):
    im, y = slide(s, n, total)
    if s['tipo'] == 'capa': return im
    limite = 1130 if s.get('nota') else 1210
    desl = max(0, (limite - y) // 2)  # centraliza o bloco entre o topo e o rodapé
    return slide(s, n, total, 230 + desl)[0] if desl else im

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    for i, s in enumerate(spec, 1):
        render(s, i, len(spec)).save(os.path.join(out, f'slide-{i:02d}.jpg'), quality=94)
    print('ok', len(spec))
