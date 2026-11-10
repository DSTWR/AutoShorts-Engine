# DSTWR AutoShorts Engine

## Current engine: Blender

This repository now uses Blender as its only animation/rendering engine. The legacy Pillow drawing renderer, Arabic eSpeak narration pipeline, and their workflow have been removed.

### Pipeline
1. Blender runs headlessly on an Ubuntu GitHub Actions runner.
2. A scripted 3D scene builds an original articulated character, stage, lighting, props and camera.
3. Keyframed motion creates an animated physical-comedy sequence.
4. FFmpeg encodes the rendered frames into a vertical MP4.
5. GitHub Actions uploads the MP4 as an artifact.

### Run
GitHub → Actions → **Blender Animation Engine - Proof of Concept** → Run workflow.

### Current status and limitations
This is the first Blender engine validation, not yet a finished viral-video production system. The current scene is a technical animation test. Character design, expressive acting, richer environments, story generation, sound design, quality checks and channel publishing remain future production stages.

The workflow does not publish to YouTube. No dedicated GPU is assumed; render performance depends on the GitHub-hosted CPU runner.
