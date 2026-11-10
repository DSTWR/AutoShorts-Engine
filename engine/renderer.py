"""Cinematic, multi-shot 2D short renderer. Pillow only; no GPU required."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os
from pathlib import Path

W, H, FPS = 720, 1280, 24
WHITE=(247,246,239); MUTED=(177,191,207); CYAN=(91,226,220)
GOLD=(255,195,92); INK=(10,16,29)

def font(size, bold=False):
    names = (["/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else
             ["/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])
    for p in names:
        if os.path.exists(p): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

F_TITLE=font(48,True); F_CAP=font(34,True); F_SMALL=font(22); F_LABEL=font(20,True)

def text(d, xy, value, f, fill=WHITE, anchor="mm"):
    try: d.text(xy,value,font=f,fill=fill,anchor=anchor,direction="rtl",language="ar",stroke_width=0)
    except Exception: d.text(xy,value,font=f,fill=fill,anchor=anchor)

def rr(d, box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box,radius=radius,fill=fill,outline=outline,width=width)

def gradient(top,bottom):
    im=Image.new("RGB",(W,H)); p=im.load()
    for y in range(H):
        q=y/(H-1); c=tuple(int(top[k]*(1-q)+bottom[k]*q) for k in range(3))
        for x in range(W): p[x,y]=c
    return im

def glow(im, x,y,r,color,alpha=70):
    layer=Image.new("RGBA,(W,H),(0,0,0,0)")
    d=ImageDraw.Draw(layer)
    d.ellipse((x-r,y-r,x+r,y+r),fill=(*color,alpha))
    layer=layer.filter(ImageFilter.GaussianBlur(r*.55))
    im.alpha_composite(layer)

def character(d,x,y,t,pose="point",scale=1.0):
    s=scale
    # Ground shadow
    d.ellipse((x-100*s,y+255*s,x+110*s,y+285*s),fill=(4,8,18,100))
    # Legs and shoes
    swing=math.sin(t*5)*13
    d.line((x-35*s,y+170*s,x-48*s+swing,y+255*s),fill=(32,43,65),width=max(8,int(25*s)))
    d.line((x+35*s,y+170*s,x+48*s-swing,y+255*s),fill=(32,43,65),width=max(8,int(25*s)))
    d.ellipse((x-83*s,y+242*s,x-27*s,y+267*s),fill=(12,18,30))
    d.ellipse((x+24*s,y+242*s,x+80*s,y+267*s),fill=(12,18,30))
    # Torso, jacket and collar
    d.rounded_rectangle((x-76*s,y+38*s,x+76*s,y+190*s),radius=int(35*s),fill=(35,105,128),outline=(113,220,215),width=max(2,int(4*s)))
    d.polygon([(x-35*s,y+43*s),(x,y+85*s),(x+34*s,y+43*s),(x+17*s,y+130*s),(x,y+111*s),(x-17*s,y+130*s)],fill=(220,232,225))
    d.line((x,y+90*s,x,y+174*s),fill=(17,52,72),width=max(2,int(4*s)))
    # Arms with pose changes
    if pose=="surprise":
        arms=[(x-65*s,y+65*s,x-125*s,y+4*s),(x+65*s,y+65*s,x+125*s,y+4*s)]
    elif pose=="think":
        arms=[(x-65*s,y+70*s,x-112*s,y+130*s),(x+65*s,y+70*s,x+36*s,y-8*s)]
    else:
        arms=[(x-65*s,y+70*s,x-125*s,y+120*s),(x+65*s,y+70*s,x+130*s,y+28*s)]
    for ax,ay,bx,by in arms:
        d.line((ax,ay,bx,by),fill=(35,105,128),width=max(9,int(27*s)))
        d.ellipse((bx-13*s,by-13*s,bx+13*s,by+13*s),fill=(220,164,119))
    # Neck and head
    d.rounded_rectangle((x-23*s,y+12*s,x+23*s,y+65*s),radius=12,fill=(202,145,105))
    d.ellipse((x-70*s,y-115*s,x+70*s,y+28*s),fill=(231,177,133),outline=(255,220,184),width=max(2,int(4*s)))
    # Hair silhouette
    d.pieslice((x-74*s,y-128*s,x+74*s,y-5*s),180,355,fill=(30,28,39))
    d.ellipse((x-69*s,y-86*s,x-35*s,y-25*s),fill=(30,28,39))
    # Brows, eyes and mouth
    blink=(math.sin(t*3.4)>0.985)
    for ex in (-27,27):
        d.line((x+(ex-11)*s,y-48*s,x+(ex+10)*s,y-51*s),fill=(62,43,43),width=max(2,int(5*s)))
        if blink: d.line((x+(ex-7)*s,y-30*s,x+(ex+7)*s,y-30*s),fill=(38,38,48),width=max(2,int(4*s)))
        else: d.ellipse((x+(ex-5)*s,y-37*s,x+(ex+5)*s,y-20*s),fill=(31,39,49))
    if pose=="surprise":
        d.ellipse((x-10*s,y-1*s,x+10*s,y+22*s),outline=(105,48,47),width=max(2,int(4*s)))
    else:
        d.arc((x-17*s,y-5*s,x+17*s,y+23*s),10,165,fill=(125,55,54),width=max(2,int(4*s)))

def desk_scene(im,t,kind):
    d=ImageDraw.Draw(im,"RGBA")
    # Window and moonlit city
    rr(d,(58,210,662,670),28,(15,29,51,230),(95,142,166,150),3)
    d.rectangle((75,230,645,650),fill=(16,37,61,255))
    for i in range(13):
        bx=90+i*43; bh=75+(i*37)%170
        d.rectangle((bx,650-bh,bx+27,650),fill=(24,51,75,255))
        for wy in range(0,bh-15,28):
            d.rectangle((bx+7,650-bh+wy+8,bx+12,650-bh+wy+14),fill=(238,184,102,180))
    d.ellipse((475,275,555,355),fill=(244,218,166,235))
    d.line((360,230,360,650),fill=(110,150,170,170),width=5)
    d.line((75,460,645,460),fill=(110,150,170,170),width=5)
    # Desk
    d.polygon([(0,790),(720,760),(720,1030),(0,1060)],fill=(65,42,42,255))
    d.polygon([(0,790),(720,760),(720,810),(0,842)],fill=(132,83,60,255))
    # table edge highlight
    d.line((0,792,720,762),fill=(205,145,97,210),width=5)
    # cup, saucer and spoon
    cx,cy=360,742
    d.ellipse((cx-78,cy+35,cx+78,cy+72),fill=(10,14,25,130))
    d.ellipse((cx-65,cy+18,cx+65,cy+52),fill=(220,226,224,255),outline=(255,255,255,255),width=4)
    d.rounded_rectangle((cx-48,cy-65,cx+48,cy+35),radius=14,fill=(231,236,229,255),outline=(255,255,255,255),width=4)
    d.ellipse((cx-48,cy-78,cx+48,cy-48),fill=(77,48,38,255),outline=(255,255,255,255),width=4)
    d.ellipse((cx+34,cy-45,cx+93,cy+15),outline=(230,238,232,255),width=13)
    d.line((cx-120,cy+26,cx-75,cy-4),fill=(205,211,208,255),width=7)
    # phone and lamp
    rr(d,(525,790,625,930),14,(17,25,39,255),(125,155,174,255),4)
    d.rounded_rectangle((536,805,614,907),radius=7,fill=(65,155,165,255))
    d.ellipse((80,670,230,820),fill=(255,187,85,24))
    d.line((155,730,155,570),fill=(38,47,63,255),width=13)
    d.polygon([(90,585),(220,585),(190,535),(120,535)],fill=(242,177,82,255))
    d.ellipse((125,575,185,635),fill=(255,213,130,90))
    # Character position shifts per shot
    if kind=="intro": character(d,175,620,t,"point",.88)
    elif kind=="change": character(d,185,620,t,"surprise",.88)
    elif kind=="reveal": character(d,545,610,t,"think",.86)
    elif kind=="demo": character(d,180,610,t,"think",.88)
    else: character(d,360,620,t,"point",.9)
    # Highlight the object being watched
    pulse=4+int(4*(1+math.sin(t*5)))
    d.ellipse((cx-88-pulse,cy-91-pulse,cx+102+pulse,cy+82+pulse),outline=(91,226,220,190),width=3)
    if kind=="change":
        # The phone screen changes while viewer attention stays on cup
        rr(d,(510,785,640,940),20,(255,190,82,80),(255,205,120,220),5)
        text(d,(575,860),"؟",F_TITLE,GOLD)
    if kind=="reveal":
        # Empty space where a small object had been
        d.ellipse((505,690,635,820),outline=(255,195,92,230),width=5)
        text(d,(570,755),"!",F_TITLE,GOLD)
    if kind=="demo":
        # Visual focus beam
        d.arc((260,620,460,820),195,345,fill=(91,226,220,220),width=5)

def frame(index,total,story,out):
    t=index/FPS
    scene=next((s for s in story["scenes"] if s["start"]<=t<s["end"]),story["scenes"][-1])
    kind=scene["visual"]
    # Different color grade per shot
    palettes={
      "intro":((9,17,34),(29,54,76)),
      "change":((18,16,35),(66,43,58)),
      "reveal":((8,25,39),(26,73,78)),
      "demo":((22,17,34),(62,51,70)),
      "end":((8,19,34),(24,57,70))}
    top,bottom=palettes[kind]
    im=gradient(top,bottom).convert("RGBA")
    d=ImageDraw.Draw(im,"RGBA")
    # Ambient light shafts
    for i in range(5):
        x=(i*190+int(t*17))%900-90
        d.polygon([(x,0),(x+75,0),(x+260,900),(x+130,900)],fill=(110,210,210,9))
    desk_scene(im,t,kind)
    d=ImageDraw.Draw(im,"RGBA")
    # Editorial top line and scene indicator
    rr(d,(38,48,682,60),6,(255,255,255,38))
    d.rounded_rectangle((38,48,38+int(644*t/30),60),radius=6,fill=(*CYAN,235))
    text(d,(W//2,112),"اختبار الانتباه  /  01",F_LABEL,(158,218,220))
    # Scene caption in a cinematic lower-third
    rr(d,(34,1000,686,1190),30,(5,12,24,222),(100,180,184,130),2)
    text(d,(W//2,1055),scene["caption"],F_CAP,WHITE)
    text(d,(W//2,1128),"راقب التفاصيل…",F_SMALL,(167,193,205))
    # Cut transition vignette
    vign=Image.new("RGBA",(W,H),(0,0,0,0)); vd=ImageDraw.Draw(vign)
    for k in range(12):
        a=3+k*2
        vd.rectangle((k*8,k*8,W-k*8,H-k*8),outline=(0,0,0,a),width=18)
    im.alpha_composite(vign)
    im.convert("RGB").save(out,quality=94)

def render_frames(story,folder,duration=30):
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=True)
    total=duration*FPS
    for i in range(total):
        frame(i,total,story,folder/f"frame_{i:05d}.jpg")
    return total
