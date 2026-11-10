# AutoShorts Engine

A zero-budget-oriented starter for producing original vertical animated Shorts with a repeatable GitHub Actions workflow.

## What it currently does

- Renders an original 2D mascot scene frame-by-frame with Python and Pillow.
- Generates Arabic narration offline using eSpeak NG when the Arabic voice is available.
- Assembles a vertical MP4 (9:16) with FFmpeg.
- Runs manually or on a daily GitHub Actions schedule and stores the MP4 as a downloadable workflow artifact.

## Run locally

Requires Python 3.11+, FFmpeg, eSpeak NG, and an Arabic-capable font.

```bash
pip install -r requirements.txt
python -m engine.build
```

Output: `output/autoshorts-demo.mp4`

## Run on GitHub

Open **Actions → AutoShorts - Build Demo → Run workflow**. The scheduled workflow runs daily at 02:30 UTC. Download the `autoshorts-demo` artifact from the completed run.

## Current scope and honest limitations

This first engine is a deterministic animation prototype, not a text-to-video model. It proves the render, voice, and assembly pipeline without a GPU. GitHub-hosted runners do not provide a free dedicated GPU. AI story generation, richer character rigs, external GPU inference, YouTube OAuth, and automatic publishing are separate future stages and are not enabled yet.

Do not put API keys or OAuth tokens in source files. Use GitHub Actions Secrets only after configuring the integrations. Uploading to YouTube is not enabled by this workflow.

## Project layout

- `engine/story.py`: editable demo story.
- `engine/renderer.py`: 2D character and scene animation.
- `engine/voice.py`: offline narration.
- `engine/build.py`: video assembly.
- `.github/workflows/build-short.yml`: build automation.
