import os
from pathlib import Path
from typing import Optional
import requests


class AvatarDriver:
    """
    Drives a static character portrait with synthesized audio
    via LivePortrait, SadTalker API or local script.
    """

    def __init__(self, api_url: Optional[str] = None):
        self.api_url = api_url or "http://127.0.0.1:8890"

    def drive(self, image_path: str, audio_path: str, output_path: str) -> Optional[str]:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        if not os.path.exists(image_path) or not os.path.exists(audio_path):
            print(f"[AvatarDriver] Input image or audio missing.")
            return None

        # Check if local LivePortrait / SadTalker API service is reachable
        try:
            with open(image_path, "rb") as img_f, open(audio_path, "rb") as aud_f:
                files = {
                    "image": img_f,
                    "audio": aud_f
                }
                res = requests.post(f"{self.api_url}/generate", files=files, timeout=120)
                if res.status_code == 200:
                    with open(output_path, "wb") as out_f:
                        out_f.write(res.content)
                    return output_path
        except Exception:
            # Service not running locally, skip video rendering and let audio play
            pass

        return None
