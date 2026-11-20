import os
import json
import asyncio
import requests
import urllib.parse
from pathlib import Path
from typing import Optional


class VoiceClient:
    """
    Synthesizes speech using edge-tts (fallback) or a local GPT-SoVITS v2 API.
    """

    def __init__(
        self,
        voice_type: str = "edge-tts",
        voice_id: str = "zh-CN-YunxiNeural",
        api_url: Optional[str] = None,
        model_dir: Optional[str] = None
    ):
        self.voice_type = voice_type
        self.voice_id = voice_id
        self.api_url = (api_url or "http://127.0.0.1:9880").rstrip("/")
        self.model_dir = Path(model_dir) if model_dir else None

    async def _synthesize_edge_tts(self, text: str, output_path: str):
        import edge_tts
        edge_voice = self.voice_id if self.voice_id.startswith("zh-") else "zh-CN-YunxiNeural"
        communicate = edge_tts.Communicate(text, edge_voice)
        await communicate.save(output_path)

    def _setup_gpt_sovits_model(self):
        """Loads specific GPT and SoVITS weights into the active API service."""
        if not self.model_dir or not self.model_dir.exists():
            return

        gpt_path = self.model_dir / "gpt.ckpt"
        sovits_path = self.model_dir / "sovits.pth"

        if gpt_path.exists():
            url = f"{self.api_url}/set_gpt_weights?weights_path={urllib.parse.quote(str(gpt_path.resolve()))}"
            requests.get(url, timeout=30)

        if sovits_path.exists():
            url = f"{self.api_url}/set_sovits_weights?weights_path={urllib.parse.quote(str(sovits_path.resolve()))}"
            requests.get(url, timeout=30)

    def _synthesize_gpt_sovits(self, text: str, output_path: str):
        # 1. Switch weights if custom character weights exist
        self._setup_gpt_sovits_model()

        # 2. Extract reference prompt settings from model_dir config.json
        ref_audio_path = ""
        prompt_text = ""
        prompt_lang = "zh"

        if self.model_dir and (self.model_dir / "config.json").exists():
            with open(self.model_dir / "config.json", "r", encoding="utf-8") as f:
                conf = json.load(f)
                ref_wav_name = conf.get("reference_wav", "ref.wav")
                ref_audio_path = str((self.model_dir / ref_wav_name).resolve())
                prompt_text = conf.get("reference_prompt", "")
                prompt_lang = conf.get("reference_language", "zh")

        payload = {
            "text": text,
            "text_lang": "zh",
            "ref_audio_path": ref_audio_path,
            "prompt_text": prompt_text,
            "prompt_lang": prompt_lang,
            "top_k": 5,
            "top_p": 1,
            "temperature": 1.0,
            "speed_factor": 1.0
        }

        res = requests.post(
            f"{self.api_url}/tts",
            json=payload,
            timeout=120
        )
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
            with open(output_path, "wb") as f:
                f.write(b"")

        return output_path
