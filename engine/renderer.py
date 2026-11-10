from PIL import Image, ImageDraw, ImageFont
import math, os
from pathlib import Path

W, H, FPS = 720, 1280, 24
BG1=(14,20,42); BG2=(34,49,83); CYAN=(90,220,225); YELLOW=(255,207,92); WHITE=(248,248,252)

def font(size):
    candidates = [
        "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def rtl(draw, xy, text, f, fill=WHITE):
    try:
        draw.text(xy, text, font=f, fill=fill, anchor="mm", direction="rtl", language="ar")
    except (TypeError, ValueError):
        draw.text(xy, text, font=f, fill=fill, anchor="mm")

def make_background():
    # Build the gradient once, not once per frame.
    im=Image.new("RGB",(W,H))
    d=ImageDraw.Draw(im)
    for y in range(H):
        q=y/H
        c=tuple(int(BG1[k]*(1-q)+BG2[k]*q) for k in range(3))
        d.line((0,y,W,y),fill=c)
    return im

BACKGROUND=make_background()
TITLE_FONT=font(38)
CAPTION_FONT=font(31)

def frame(index, total, title, hook, lines, out):
    t=index/FPS
    phase=min(1, index/max(1,total-1))
    im=BACKGROUND.copy()
    d=ImageDraw.Draw(im,"RGBA")
    for j in range(9):
        x=int((j*113 + t*22)%(W+180))-90
        y=int(120+j*137+math.sin(t+j)*24)
        r=18+(j%3)*12
        d.ellipse((x-r,y-r,x+r,y+r), fill=(*CYAN,22), outline=(*CYAN,45), width=2)
    rtl(d,(W//2,115),title,TITLE_FONT,YELLOW)
    cx=W//2 + int(math.sin(t*2)*20)
    cy=590 + int(math.sin(t*4)*12)
    d.ellipse((cx-135,cy+250,cx+135,cy+292),fill=(0,0,0,65))
    d.rounded_rectangle((cx-105,cy+35,cx+105,cy+260),radius=70,fill=(57,166,190),outline=(190,250,250),width=6)
    d.ellipse((cx-145,cy-145,cx+145,cy+145),fill=(245,190,132),outline=(255,235,205),width=7)
    d.ellipse((cx-172,cy-25,cx-125,cy+40),fill=(245,190,132))
    d.ellipse((cx+125,cy-25,cx+172,cy+40),fill=(245,190,132))
    blink=(int(t*2.2)%9==0 and (t*2.2)%1<0.12)
    for ex in (-52,52):
        if blink: d.line((cx+ex-13,cy-25,cx+ex+13,cy-25),fill=(45,45,60),width=7)
        else: d.ellipse((cx+ex-13,cy-38,cx+ex+13,cy-8),fill=(35,39,54))
    d.arc((cx-38,cy+5,cx+38,cy+65),start=15,end=165,fill=(120,55,55),width=6)
    swing=int(math.sin(t*3)*24)
    d.line((cx-90,cy+100,cx-165,cy+175+swing),fill=(245,190,132),width=28)
    d.line((cx+90,cy+100,cx+165,cy+175-swing),fill=(245,190,132),width=28)
    all_text=[hook]+lines
    slot=min(len(all_text)-1, int(phase*len(all_text)))
    d.rounded_rectangle((42,940,678,1150),radius=32,fill=(7,12,29,205),outline=(*CYAN,150),width=3)
    rtl(d,(360,1045),all_text[slot],CAPTION_FONT,WHITE)
    d.rounded_rectangle((42,1200,678,1212),radius=6,fill=(255,255,255,55))
    d.rounded_rectangle((42,1200,42+int(636*phase),1212),radius=6,fill=CYAN)
    im.save(out)

def render_frames(story, folder, duration=18):
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=True)
    total=duration*FPS
    for i in range(total):
        frame(i,total,story["title"],story["hook"],story["lines"],folder/f"frame_{i:05d}.png")
    return total
