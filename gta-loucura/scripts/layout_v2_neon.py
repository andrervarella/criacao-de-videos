from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math
W,H=1080,1920
PINK=(255,36,145); CYAN=(45,230,240); WHITE=(255,255,255); DARK=(22,6,36); RED=(255,59,59); GOLD=(255,200,60)
MI='/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat-Italic[wght].ttf'
MR='/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf'
def f(size,w='Black',italic=True):
    ft=ImageFont.truetype(MI if italic else MR,size)
    ft.set_variation_by_name((w+' Italic') if italic and w!='Italic' else w)
    return ft
def glow(base,layer,radius=18,strength=2):
    g=layer.filter(ImageFilter.GaussianBlur(radius))
    for _ in range(strength): base.alpha_composite(g)
    base.alpha_composite(layer)
# ---------- fundo: céu synthwave ----------
bg=Image.new('RGBA',(W,H))
top=(14,4,28); mid=(58,10,78); hor=(150,25,120)
px=bg.load()
for y in range(H):
    t=y/H
    if t<0.62: k=t/0.62; c=[int(top[i]+(mid[i]-top[i])*k) for i in range(3)]
    elif t<0.74: k=(t-0.62)/0.12; c=[int(mid[i]+(hor[i]-mid[i])*k) for i in range(3)]
    else: k=(t-0.74)/0.26; c=[int(hor[i]+(top[i]-hor[i])*min(1,k*1.3)) for i in range(3)]
    for x in range(W): px[x,y]=(*c,255)
# sol listrado atrás da faixa inferior
sun=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sun)
cx,cy,r=540,1420,300
for y in range(cy-r,cy+1):
    t=(y-(cy-r))/r
    col=(255,int(190-150*t),int(80+60*t),150)
    dx=int(math.sqrt(max(0,r*r-(y-cy)**2)))
    band=(y-(cy-r))
    if band>r*0.45 and (band//14)%2==1: continue
    sd.line([(cx-dx,y),(cx+dx,y)],fill=col)
glow(bg,sun,30,1)
# grade de chão em perspectiva
grid=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(grid)
hy=1420
for i in range(-14,15):
    gd.line([(540+i*30,hy),(540+i*260,H)],fill=(*CYAN,70),width=2)
y=hy; step=8
while y<H:
    gd.line([(0,y),(W,y)],fill=(*CYAN,int(40+60*(y-hy)/(H-hy))),width=2); step*=1.28; y+=step
bg.alpha_composite(grid)
# skyline sutil
sk=Image.new('RGBA',(W,H),(0,0,0,0)); kd=ImageDraw.Draw(sk)
import random; random.seed(6); x=0
while x<W:
    w=random.randint(40,90); h=random.randint(60,230)
    kd.rectangle([x,hy-h,x+w,hy],fill=(30,6,48,235))
    for wy in range(hy-h+14,hy-10,22):
        for wx in range(x+8,x+w-8,18):
            if random.random()<0.25: kd.rectangle([wx,wy,wx+6,wy+8],fill=(*PINK,140) if random.random()<.5 else (*CYAN,120))
    x+=w+random.randint(2,10)
bg.alpha_composite(sk)
# vinheta + scanlines
vg=Image.new('L',(W,H),0); vd=ImageDraw.Draw(vg); vd.ellipse([-300,-200,W+300,H+200],fill=255)
vg=ImageChops.invert(vg.filter(ImageFilter.GaussianBlur(160)))
bg.alpha_composite(Image.merge('RGBA',[Image.new('L',(W,H),0)]*3+[vg.point(lambda v:int(v*0.7))]))
sl=Image.new('RGBA',(W,H),(0,0,0,0)); sld=ImageDraw.Draw(sl)
for y in range(0,H,4): sld.line([(0,y),(W,y)],fill=(0,0,0,28))
bg.alpha_composite(sl)
im=bg; d=ImageDraw.Draw(im)
# ---------- topo ----------
logo=Image.open('../logo/plaquinha-gta-loucura.png'); lw=330
logo=logo.resize((lw,int(logo.height*lw/logo.width)),Image.LANCZOS)
sh=Image.new('RGBA',(W,H),(0,0,0,0)); sh.paste((255,36,145,255),(40,128),logo); sh=sh.filter(ImageFilter.GaussianBlur(22))
im.alpha_composite(sh); im.alpha_composite(sh); im.alpha_composite(logo,(40,120))
# HUD direita: "CORTE DO DIA" + estrelas de procurado
def star(dr,cx,cy,R,fill,outline=None):
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rr=R if i%2==0 else R*0.45
        pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
    dr.polygon(pts,fill=fill,outline=outline)
hud=Image.new('RGBA',(W,H),(0,0,0,0)); hd=ImageDraw.Draw(hud)
for i in range(5): star(hd,690+i*62,190,24,(*WHITE,255) if i<4 else (*WHITE,70))
glow(im,hud,8,1)
ft=f(30,'ExtraBold'); txt='CORTE DO DIA #001'
tw=d.textlength(txt,font=ft); x1=1040; x0=x1-tw-44
d.rounded_rectangle([x0,232,x1,282],radius=25,outline=CYAN,width=3,fill=(10,4,24,200))
d.text(((x0+x1)/2,257),txt,font=ft,fill=CYAN,anchor='mm')
# ---------- etiqueta + título ----------
def para(x,y,w,h,fill,sk=16): d.polygon([(x+sk,y),(x+w,y),(x+w-sk,y+h),(x,y+h)],fill=fill)
ft=f(32,'ExtraBold'); txt='CORTE DE LIVE  •  ROBIN HOOD GAMER'
tw=d.textlength(txt,font=ft)
para(40,380,tw+110,56,PINK)
d.polygon([(68,396),(68,420),(88,408)],fill=DARK)
d.text((102,408),txt,font=ft,fill=DARK,anchor='lm')
def shadow_text(xy,text,font,fill,shadow=(10,0,20,255),off=6,g=None):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); ld=ImageDraw.Draw(lay)
    ld.text((xy[0]+off,xy[1]+off),text,font=font,fill=shadow,anchor='lm')
    im.alpha_composite(lay)
    t=Image.new('RGBA',(W,H),(0,0,0,0)); td=ImageDraw.Draw(t); td.text(xy,text,font=font,fill=fill,anchor='lm')
    if g: glow(im,t,g,1)
    else: im.alpha_composite(t)
shadow_text((40,506),'EMPURRAR UM JET SKI',f(74),(*WHITE,255))
shadow_text((40,612),'VIROU MISSÃO!',f(118),(*PINK,255),g=16)
# ---------- janela do vídeo ----------
VX0,VY0,VX1,VY1=40,700,1040,1262
fr=Image.new('RGBA',(W,H),(0,0,0,0)); frd=ImageDraw.Draw(fr)
frd.rounded_rectangle([VX0-6,VY0-6,VX1+6,VY1+6],radius=34,outline=(*CYAN,255),width=6)
glow(im,fr,22,2)
d.rounded_rectangle([VX0,VY0,VX1,VY1],radius=28,fill=(12,10,22,255))
# placeholder
cxv,cyv=(VX0+VX1)//2,(VY0+VY1)//2
d.ellipse([cxv-60,cyv-90,cxv+60,cyv+30],outline=(255,255,255,120),width=5)
d.polygon([(cxv-18,cyv-58),(cxv-18,cyv-2),(cxv+30,cyv-30)],fill=(255,255,255,140))
d.text((cxv,cyv+80),'SEU CORTE AQUI  •  16:9',font=f(34,'Bold'),fill=(255,255,255,120),anchor='mm')
# cantoneiras rosa
for (x,y,sx,sy) in [(VX0-22,VY0-22,1,1),(VX1+22,VY0-22,-1,1),(VX0-22,VY1+22,1,-1),(VX1+22,VY1+22,-1,-1)]:
    d.line([(x,y),(x+sx*60,y)],fill=PINK,width=8); d.line([(x,y),(x,y+sy*60)],fill=PINK,width=8)
# selo AO VIVO no vídeo
d.rounded_rectangle([VX0+24,VY0+24,VX0+190,VY0+72],radius=10,fill=RED)
d.ellipse([VX0+40,VY0+40,VX0+56,VY0+56],fill=WHITE)
d.text((VX0+66,VY0+48),'AO VIVO',font=f(28,'Black'),fill=WHITE,anchor='lm')
# ---------- abaixo do vídeo ----------
band=Image.new('RGBA',(W,H),(0,0,0,0)); bd=ImageDraw.Draw(band); bd.rectangle([0,1290,W,1425],fill=(14,4,28,200)); im.alpha_composite(band.filter(ImageFilter.GaussianBlur(14))); d=ImageDraw.Draw(im)
fb=f(40,'Bold',italic=False)
d.text((44,1312),'Tentou de tudo pra pôr o jet ski na água…',font=fb,fill=WHITE)
d.text((44,1362),'até apelar pro chute. E funcionou!',font=fb,fill=(255,190,225))
y=1450; bw=890
para(54,y+14,bw,104,CYAN,24); para(40,y,bw,104,PINK,24)
d.text((40+bw/2,y+52),'NO GTA 6 ATÉ O CHUTE É FÍSICA',font=f(46),fill=DARK,anchor='mm')
# crédito em pílula (dentro da área segura)
ft=f(26,'SemiBold',italic=False); txt='FONTE: LIVE ROBIN HOOD GAMER E HEYDAVI • 18.11.2026'
tw=d.textlength(txt,font=ft)
d.rounded_rectangle([40,1590,40+tw+40,1636],radius=23,fill=(10,4,24,210),outline=(*CYAN,180),width=2)
d.text((60,1613),txt,font=ft,fill=(225,215,240),anchor='lm')
im.convert('RGB').save('layout_v2.png')
# ---------- versão com guias da área segura ----------
g=im.copy(); ov=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(ov)
gd.rectangle([0,0,W,100],fill=(255,0,0,90)); gd.rectangle([0,1660,W,H],fill=(255,0,0,90)); gd.rectangle([950,1050,W,1660],fill=(255,0,0,90))
fl=f(30,'Bold',italic=False)
gd.text((W/2,50),'topo do app',font=fl,fill=WHITE,anchor='mm')
gd.text((W/2,1790),'legenda e nome do perfil (Instagram cobre)',font=fl,fill=WHITE,anchor='mm')
gd.text((1015,1355),'botões',font=f(24,'Bold',italic=False),fill=WHITE,anchor='mm')
g.alpha_composite(ov); g.convert('RGB').save('layout_v2_area_segura.png')
side=Image.new('RGB',(1080+40+1080,1920),(0,0,0)); side.paste(im.convert('RGB'),(0,0)); side.paste(g.convert('RGB'),(1120,0))
side.resize((1100,960)).save('comparativo.jpg',quality=88)
