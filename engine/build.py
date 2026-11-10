import json, os, shutil, subprocess
from pathlib import Path
from .story import STORY
from .renderer import render_frames, FPS
from .voice import make_voice

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"output"
FRAMES=OUT/"frames"

def run(cmd):
    subprocess.run(cmd,check=True)

def main():
    OUT.mkdir(exist_ok=True)
    for p in (FRAMES,):
        if p.exists(): shutil.rmtree(p)
        p.mkdir(parents=True)
    duration=int(os.getenv("VIDEO_DURATION","18"))
    render_frames(STORY,FRAMES,duration)
    text=" ".join([STORY["hook"],*STORY["lines"],STORY["outro"]])
    audio=OUT/"voice.wav"
    voice_ok=make_voice(text,audio)
    video=OUT/"autoshorts-demo.mp4"
    cmd=["ffmpeg","-y","-framerate",str(FPS),"-i",str(FRAMES/"frame_%05d.png")]
    if voice_ok:
        cmd += ["-i",str(audio),"-c:a","aac","-shortest"]
    else:
        cmd += ["-f","lavfi","-i",f"anullsrc=r=44100:cl=stereo","-c:a","aac","-shortest"]
    cmd += ["-c:v","libx264","-pix_fmt","yuv420p","-vf","format=yuv420p","-r",str(FPS),"-movflags","+faststart",str(video)]
    run(cmd)
    metadata={"title":STORY["title"],"file":str(video.relative_to(ROOT)),"duration_seconds":duration,"voice_generated":voice_ok,"format":"9:16"}
    (OUT/"metadata.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(metadata,ensure_ascii=False))
if __name__=="__main__": main()
