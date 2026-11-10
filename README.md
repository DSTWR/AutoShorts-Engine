# AutoShorts Engine

A zero-budget-oriented 2D short-film renderer running on GitHub Actions without a GPU.

## Current production pass
- Five storyboarded shots with distinct color grades and scene compositions.
- A recurring illustrated host with pose changes and facial animation.
- A designed environment with a night window, desk, cup, phone, lamp, shadows and focus cues.
- Arabic captions and narration, vertical 9:16 output at 720x1280 / 24 FPS.
- FFmpeg H.264 output artifact.

## Build
Open Actions → AutoShorts - Build Demo → Run workflow. The output is uploaded as `autoshorts-demo`.

## Honest limitations
This is a procedural 2D animation engine, not generative video. The character is illustrated by vector-like drawing primitives, not a hand-drawn frame animation rig. Arabic narration still depends on the locally installed eSpeak NG voice and is synthetic. This workflow does not publish to YouTube. GitHub-hosted runners do not provide a free dedicated GPU.

## Layout
- `engine/story.py`: storyboard and narration.
- `engine/renderer.py`: scene art, character poses and frame renderer.
- `engine/voice.py`: offline speech.
- `engine/build.py`: FFmpeg assembly.
- `.github/workflows/build-short.yml`: manual/scheduled build.
