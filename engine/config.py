from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    width: int = int(os.getenv("VIDEO_WIDTH", "720"))
    height: int = int(os.getenv("VIDEO_HEIGHT", "1280"))
    fps: int = int(os.getenv("VIDEO_FPS", "24"))
    duration: int = int(os.getenv("VIDEO_DURATION", "18"))
    output_dir: str = os.getenv("OUTPUT_DIR", "output")
    language: str = os.getenv("TTS_LANGUAGE", "ar")
