import subprocess
from pathlib import Path

def make_voice(text: str, output: Path, voice: str = "ar") -> bool:
    """Create speech with the locally installed espeak-ng voice."""
    result = subprocess.run(
        ["espeak-ng", "-v", voice, "-s", "148", "-w", str(output), text],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("TTS warning:", result.stderr[-1000:])
        return False
    return output.exists() and output.stat().st_size > 1000
