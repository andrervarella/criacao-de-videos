from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
BG=(21,7,34,255); PINK=(255,30,140,255); CYAN=(40,225,235,255); WHITE=(255,255,255,255)
M='/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf'
def f(size,w='ExtraBold'):
    ft=ImageFont.truetype(M,size)
    try: ft.set_variation_by_name(w)
    except Exception: pass
    return ft
VY0,VY1=656,1264  # janela do vídeo 16:9
im=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(im)
d.rectangle([0,VY0,W,VY1],fill=(0,0,0,0))  # janela transparente
# logo
logo=Image.open('../logo/plaquinha-gta-loucura.png'); lw=330; logo=logo.resize((lw,int(logo.height*lw/logo.width)),Image.LANCZOS)
im.alpha_composite(logo,(40,48))
# linha ciano + detalhe rosa
d.rectangle([400,150,1000,155],fill=CYAN); d.polygon([(985,138),(1040,138),(1020,170),(965,170)],fill=PINK)
# etiqueta
def tag(y,text,size=34,x=40):
    ft=f(size); tw=d.textlength(text,font=ft); h=size+26
    d.polygon([(x+12,y),(x+tw+52,y),(x+tw+40,y+h),(x,y+h)],fill=PINK)
    d.text((x+26,y+h/2),text,font=ft,fill=(30,5,40,255),anchor='lm')
tag(300,'AO VIVO • PRIMEIRO DIA DE GTA 6')
# título
d.rectangle([40,385,52,620],fill=PINK)
d.text((72,440),'EMPURRAR UM JET SKI',font=f(72,'Black'),fill=WHITE,anchor='lm')
d.text((72,540),'VIROU MISSÃO!',font=f(96,'Black'),fill=PINK,anchor='lm')
# legenda abaixo do vídeo
ft=f(38,'SemiBold')
d.text((60,1310),'Ele tentou de tudo pra botar o jet ski na água…',font=ft,fill=WHITE)
d.text((60,1360),'até apelar pro chute. E não é que funcionou?',font=ft,fill=WHITE)
# faixa rosa com sombra ciano
y=1460; d.polygon([(52,y+14),(1052,y+14),(1022,y+124),(22,y+124)],fill=CYAN)
d.polygon([(40,y),(1040,y),(1010,y+110),(10,y+110)],fill=PINK)
d.text((525,y+55),'NO GTA 6 ATÉ O CHUTE É FÍSICA',font=f(52,'Black'),fill=(30,5,40,255),anchor='mm')
# rodapé
d.rectangle([40,1680,1040,1683],fill=CYAN)
fr=f(28,'Medium')
d.text((48,1712),'LIVE: ROBIN HOOD GAMER E HEYDAVI • YOUTUBE @ROBINLIVE',font=fr,fill=(220,210,235,255))
d.text((48,1752),'18.11.2026 • GTA LOUCURA',font=fr,fill=(220,210,235,255))
d.text((1040,1752),'@gta6_loucura',font=f(30,'Bold'),fill=PINK,anchor='ra')
im.save('moldura_gta_loucura_1080x1920.png')
# prévia com frame fake
pv=Image.new('RGBA',(W,H),(60,90,120,255)); pv.alpha_composite(im); pv.convert('RGB').resize((540,960)).save('previa.jpg')
