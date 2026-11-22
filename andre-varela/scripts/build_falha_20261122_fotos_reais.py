#!/usr/bin/env python3
# Carrossel AV: falha muscular, fotos reais com fontes públicas e gráfico fiel a Wu et al. (2026).
# Nenhuma imagem de pessoa é gerada por IA; todas são fotos reais com licenças indicadas em CREDITOS.md.
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter
from io import BytesIO
from pathlib import Path
import requests, math, time
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"andre-varela/posts/2026-11-22-falha-muscular-reais-v1"
OUT.mkdir(parents=True,exist_ok=True)
W,H=1080,1350
BG=(13,15,19);CARD=(27,29,34);RED=(170,21,31);R2=(211,34,50);WHITE=(246,246,246);SILVER=(196,202,207);MUTED=(160,168,175)
FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def ff(s,b=False):return ImageFont.truetype(FB if b else FR,s)
def T(draw,xy,text,size=30,color=WHITE,b=False,spacing=7):draw.multiline_text(xy,text,font=ff(size,b),fill=color,spacing=spacing)
def DL(draw,x,y,parts,size=58):
 for label,color in parts:
  T(draw,(x,y),label,size,color,True);y+=int(size*1.3)
def fit(im,w,h,fx=.5,fy=.5):
 iw,ih=im.size;scale=max(w/iw,h/ih);im=im.resize((round(iw*scale),round(ih*scale)),Image.Resampling.LANCZOS)
 ox=round((im.width-w)*fx);oy=round((im.height-h)*fy);return im.crop((ox,oy,ox+w,oy+h))
def darken(im,degree=.78):
 return ImageEnhance.Brightness(im).enhance(degree)
def dl(url,name):
 p=OUT/name
 if p.exists():return Image.open(p).convert("RGB")
 headers={"User-Agent":"AVResearchCarousel/1.0 (+https://github.com/andrervarella/criacao-de-videos)", "Accept":"image/avif,image/webp,image/*,*/*;q=0.8"}
 for _ in range(3):
  try:
   r=requests.get(url,headers=headers,timeout=25,allow_redirects=True);r.raise_for_status()
   img=Image.open(BytesIO(r.content)).convert("RGB")
   if min(img.size)<250:raise ValueError("resolução baixa")
   img.thumbnail((1800,1800),Image.Resampling.LANCZOS);img.save(p,quality=91)
   return img
  except Exception as e:
   print("Download falhou:",name,str(e));time.sleep(2)
 raise RuntimeError("Não foi possível obter foto REAL: "+url)
# Fontes Pexels License, ver CREDITOS.md (fotografias de pessoas, não participantes dos estudos).
photo={
"capa":("https://images.pexels.com/photos/7289304/pexels-photo-7289304.jpeg?auto=compress&cs=tinysrgb&w=1700","foto-real-capa.jpg"),
"agachamento":("https://images.pexels.com/photos/5327530/pexels-photo-5327530.jpeg?auto=compress&cs=tinysrgb&w=1400","foto-real-agachamento.jpg"),
"supino":("https://commons.wikimedia.org/wiki/Special:Redirect/file/Bench_Press_-_Flickr_-_colros.jpg","foto-real-supino.jpg"),
"extensora":("https://images.pexels.com/photos/19722966/pexels-photo-19722966.jpeg?auto=compress&cs=tinysrgb&w=1400","foto-real-extensora.jpg"),
"terra":("https://commons.wikimedia.org/wiki/Special:Redirect/file/Fit_young_man_doing_deadlift_exercise_in_gym.jpg","foto-real-terra.jpg")}
P={}
for k,(u,n) in photo.items():P[k]=dl(u,n)
logo=Image.open(ROOT/"andre-varela/logo/logo-av.png").convert("RGBA")
# Crop logo using alpha or matte; preserve its precise pixels.
if logo.getextrema()[-1]==(255,255):
 rgba=logo.convert("RGBA")
 import numpy as np
 aa=np.asarray(rgba).copy()
 mask=(aa[:,:,:3].max(axis=2)>11)
 aa[:,:,3]=(mask*255).astype("uint8")
 logo=Image.fromarray(aa,"RGBA")
bb=logo.getbbox()
if bb:logo=logo.crop(bb)
def base(n):
 im=Image.new("RGB",(W,H),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,0,8,H),fill=RED);d.rectangle((68,58,78,102),fill=RED)
 T(d,(96,52),"ANDRÉ VARELA",29,WHITE,True)
 T(d,(97,100),"PERFORMANCE & EVOLUÇÃO",17,SILVER,False)
 d.line((68,170,1010,170),fill=(71,75,80),width=2)
 l=logo.copy();l.thumbnail((175,106),Image.Resampling.LANCZOS)
 im.paste(l,(W-75-l.width,46),l)
 d=ImageDraw.Draw(im)
 d.line((70,1246,1010,1246),fill=(66,68,72),width=2)
 T(d,(71,1262),"WU ET AL. • 2026 • REVISÃO SISTEMÁTICA E META-ANÁLISE",17,MUTED)
 return im
def save(im,n):im.save(OUT/("slide-%02d.jpg"%n),"JPEG",quality=92,optimize=True,subsampling=0)
def frame(d,xy,r=18):d.rounded_rectangle(xy,radius=r,outline=(74,78,82),fill=CARD,width=2)
# Slide 1: foto de verdade, sem modificar pessoas ou biomecânica
im=base(1);p=fit(P["capa"],580,920,fx=.52,fy=.5);im.paste(darken(p,.74),(500,195))
# black opacity gradient from left to right under text
overlay=Image.new("RGBA",(620,920),(13,15,19,0))
a=Image.new("L",(620,920),0);ad=ImageDraw.Draw(a)
for x in range(620):
 opacity=int(255*max(0,1-x/620)**.85)
 ad.line((x,0,x,920),fill=opacity,width=1)
overlay.putalpha(a);im=Image.alpha_composite(im.convert("RGBA"),Image.new("RGBA",im.size,(0,0,0,0))) if False else im
im.paste(overlay,(430,195),overlay)
d=ImageDraw.Draw(im)
T(d,(70,220),"CIÊNCIA DO TREINAMENTO",23,R2,True)
DL(d,70,352,[("TREINAR ATÉ",WHITE),("A FALHA",R2),("FAZ O MÚSCULO",WHITE),("CRESCER MAIS?",WHITE)],58)
d.rectangle((73,821,151,827),fill=R2)
T(d,(72,868),"O que uma análise de 20 estudos\ncientíficos encontrou?",30,WHITE)
frame(d,(70,1095,512,1171),10);T(d,(97,1117),"ARRASTE E ENTENDA  →",25,WHITE,True)
save(im,1)
# Slide 2 - equipamento como composição tipográfica (sem imagem falsa de pessoa)
im=base(2);d=ImageDraw.Draw(im)
T(d,(72,244),"NÃO FOI UM",69,WHITE,True);T(d,(72,343),"TREINO SÓ.",78,R2,True)
T(d,(72,493),"Os pesquisadores reuniram\nresultados de estudos diferentes.",31,WHITE)
for x,num,label in [(72,"20","ESTUDOS"),(552,"556","PARTICIPANTES")]:
 frame(d,(x,675,x+445,947));T(d,(x+27,703),num,124,R2 if x==72 else WHITE,True);T(d,(x+31,870),label,28,SILVER,True)
T(d,(72,1010),"Participaram iniciantes e pessoas\ncom experiência em musculação.",28,WHITE)
T(d,(72,1150),"COMO ELAS TREINARAM?  →",27,R2,True)
save(im,2)
# Slide 3 - four REAL action photos, no invented technique or study footage
im=base(3);d=ImageDraw.Draw(im)
T(d,(72,213),"COMO OS ESTUDOS",58,WHITE,True);T(d,(72,287),"FORAM CONDUZIDOS?",58,R2,True)
# summary strips
for x,top,bot in [(72,"4 A 14","SEMANAS"),(400,"2 A 4","TREINOS/SEMANA"),(735,"VARIADAS","SÉRIES E CARGAS")]:
 frame(d,(x,408,x+282,574),12);T(d,(x+17,438),top,39,R2 if x==400 else WHITE,True);T(d,(x+17,511),bot,19,SILVER,True)
T(d,(72,610),"EXEMPLOS DE EXERCÍCIOS UTILIZADOS",28,WHITE,True)
cards=[("agachamento","AGACHAMENTO"),("supino","SUPINO"),("extensora","CADEIRA EXTENSORA"),("terra","LEVANTAMENTO TERRA")]
for i,(key,label) in enumerate(cards):
 x=72+(i%2)*476;y=669+(i//2)*235
 frame(d,(x,y,x+445,y+211),12)
 ph=fit(P[key],441,147,.5,.5);im.paste(darken(ph,.85),(x+2,y+2))
 d=ImageDraw.Draw(im)
 d.rectangle((x+2,y+149,x+443,y+153),fill=R2)
 T(d,(x+16,y+165),label,23,WHITE,True)
T(d,(72,1160),"Fotos ilustrativas. Cada estudo teve seu protocolo.",19,SILVER)
save(im,3)
# Slide 4 — two approaches
im=base(4);d=ImageDraw.Draw(im)
T(d,(72,228),"O QUE FOI",63,WHITE,True);T(d,(72,307),"COMPARADO?",75,R2,True)
for y,h,sub,barclr in [(505,"ATÉ A FALHA","Parar quando não consegue\ncompletar outra repetição.",R2),(810,"ANTES DA FALHA","Parar enquanto ainda\nconseguiria repetir.",(207,211,214))]:
 frame(d,(72,y,1008,y+267))
 T(d,(104,y+34),h,43,barclr,True)
 for j in range(8 if y==505 else 6):
  d.rounded_rectangle((107+j*77,y+125,159+j*77,y+168),radius=8,fill=barclr)
 T(d,(104,y+188),sub,22,WHITE)
T(d,(72,1146),"BARRAS ILUSTRATIVAS: NÃO REPRESENTAM UM PROTOCOLO ÚNICO.",17,MUTED)
save(im,4)
# Slide 5 — endpoints
im=base(5);d=ImageDraw.Draw(im)
T(d,(70,245),"O QUE MUDOU",63,WHITE,True);T(d,(70,323),"DEPOIS DO TREINO?",59,R2,True)
rows=[("01","TAMANHO MUSCULAR","Espessura, área ou volume."),("02","FORÇA DINÂMICA","Quanto peso conseguiam mover."),("03","RESISTÊNCIA","Quantas repetições conseguiam."),("04","POTÊNCIA","Capacidade de gerar força rapidamente.")]
for i,(num,head,sub) in enumerate(rows):
 y=526+i*171;frame(d,(72,y,1008,y+145))
 T(d,(107,y+32),num,49,R2 if i==0 else MUTED,True)
 T(d,(209,y+20),head,31,WHITE,True);T(d,(209,y+84),sub,23,SILVER)
save(im,5)
# interval plot exactly from provided meta-analytic estimates, not raw group means
def graph(im,n,title,kicker,es,lo,hi,conclusion,note):
 d=ImageDraw.Draw(im)
 T(d,(72,222),kicker,26,R2,True)
 T(d,(72,321),title,61,WHITE,True)
 frame(d,(72,524,1008,955))
 T(d,(114,567),"EFEITO MÉDIO ENTRE ESTRATÉGIAS",25,SILVER)
 T(d,(117,650),"FAVORECE FALHA",19,SILVER)
 T(d,(698,650),"FAVORECE SEM FALHA",19,SILVER)
 y=742;x0=537;scale=680/1.2
 d.line((x0-340,y+31,x0+340,y+31),fill=(116,120,124),width=3)
 for v in [-.6,-.3,0,.3,.6]:
  x=round(x0+v*scale)
  d.line((x,y+17,x,y+45),fill=(120,123,125),width=2)
  T(d,(x-27,y+62),f"{v:+.1f}" if v else "0",19,SILVER)
 d.line((x0,y-67,x0,y+54),fill=R2,width=4)
 xa=round(x0+lo*scale);xb=round(x0+hi*scale);xc=round(x0+es*scale)
 d.line((xa,y,xb,y),fill=WHITE,width=9)
 for x in [xa,xb]:d.line((x,y-17,x,y+17),fill=WHITE,width=6)
 d.ellipse((xc-16,y-16,xc+16,y+16),fill=R2,outline=WHITE,width=3)
 T(d,(111,887),f"g = {es:+.2f}".replace(".",","),34,WHITE,True)
 T(d,(412,889),f"IC 95%: {lo:+.2f} a {hi:+.2f}".replace(".",","),25,WHITE)
 T(d,(72,1003),conclusion,35,WHITE,True)
 T(d,(72,1110),note,23,SILVER)
 return im
im=base(6);graph(im,6,"E A HIPERTROFIA?","RESULTADO 01 • TAMANHO MUSCULAR",-.15,-.39,.09,"SEM DIFERENÇA ESTATÍSTICA DETECTADA.","O intervalo de confiança cruza o zero.")
save(im,6)
im=base(7);graph(im,7,"E OS GANHOS DE FORÇA?","RESULTADO 02 • FORÇA DINÂMICA",.24,.06,.42,"PEQUENA VANTAGEM MÉDIA SEM FALHA.","É a média dos estudos, não uma garantia individual.")
save(im,7)
# slide 8 — biological individuality
im=base(8);d=ImageDraw.Draw(im)
T(d,(73,228),"E NA VIDA",76,WHITE,True);T(d,(73,327),"REAL?",83,R2,True)
for i,(head,sub) in enumerate([
("INICIANTE","Primeiro desenvolve técnica e percepção de esforço."),
("TREINA 3 VEZES/SEMANA","Precisa distribuir esforço e recuperação."),
("TREINA 5 VEZES/SEMANA","Também precisa administrar a fadiga.")]):
 y=537+i*179;frame(d,(76,y,1005,y+156))
 d.rectangle((76,y+11,84,y+145),fill=R2)
 T(d,(114,y+26),head,31,WHITE,True)
 T(d,(114,y+91),sub,23,SILVER)
T(d,(72,1114),"A CIÊNCIA AMPLIA O REPERTÓRIO.",28,WHITE,True)
T(d,(72,1155),"A INDIVIDUALIDADE ORIENTA A PRESCRIÇÃO.",25,R2,True)
save(im,8)
print("Criados 8 slides:",OUT)
