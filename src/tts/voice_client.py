import os
import asyncio
import requests
from pathlib import Path
from typing import Optional


class VoiceClient:
    """
    Synthesizes speech using edge-tts (built-in default) or a local GPT-SoVITS / CosyVoice API.
    """

    def __init__(self, voice_type: str = "edge-tts", voice_id: str = "zh-CN-YunxiNeural", api_url: Optional[str] = None):
        self.voice_type = voice_type
        self.voice_id = voice_id
        self.api_url = api_url or "http://127.0.0.1:9880"

    async def _synthesize_edge_tts(self, text: str, output_path: str):
        import edge_tts
        communicate = edge_tts.Communicate(text, self.voice_id)
        await communicate.save(output_path)

    def _synthesize_gpt_sovits(self, text: str, output_path: str):
        # Standard GPT-SoVITS fast_api endpoint format
        params = {
            "text": text,
            "text_language": "zh",
        }
        res = requests.get(f"{self.api_url}/tts", params=params, timeout=60)
        if res.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(res.content)
        else:
            raise RuntimeError(f"GPT-SoVITS API returned error status {res.status_code}: {res.text}")

    def synthesize(self, text: str, output_path: str) -> str:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        if self.voice_type == "gpt-sovits":
            try:
                self._synthesize_gpt_sovits(text, output_path)
                return output_path
            except Exception as e:
                print(f"[VoiceClient] GPT-SoVITS failed ({e}), falling back to edge-tts.")

        # Fallback to edge-tts
        try:
            asyncio.run(self._synthesize_edge_tts(text, output_path))
        except Exception as e:
            print(f"[VoiceClient] Edge-TTS error: {e}")
            # Create an empty or silent indicator if completely offline
            with open(output_path, "wb") as f:
                f.write(b"")

        return output_path
