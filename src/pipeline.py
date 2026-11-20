import os
import time
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

from src.config import ConfigLoader
from src.llm.agent import PersonaAgent
from src.tts.voice_client import VoiceClient
from src.video.avatar_driver import AvatarDriver


class StreamerPipeline:
    def __init__(self, config_path: str = "configs/characters.yaml"):
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.load_config()

    def run(
        self,
        character_id: str,
        user_message: str,
        generate_video: bool = False
    ) -> Dict[str, Any]:
        char_conf = self.config_loader.get_character_config(character_id)

        # 1. LLM Generation
        agent = PersonaAgent(
            system_prompt=char_conf["system_prompt"],
            character_id=character_id
        )
        reply_text = agent.chat(user_message)

        # 2. TTS Audio Synthesis
        timestamp = int(time.time())
        outputs_dir = self.config_loader.base_dir / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)
        audio_filename = str(outputs_dir / f"audio_{character_id}_{timestamp}.wav")
        
        model_dir_rel = char_conf.get("model_dir")
        model_dir_abs = (self.config_loader.base_dir / model_dir_rel) if model_dir_rel else None

        voice_client = VoiceClient(
            voice_type=char_conf.get("voice_type", "edge-tts"),
            voice_id=char_conf.get("voice_id", "zh-CN-YunxiNeural"),
            api_url=char_conf.get("tts_api_url"),
            model_dir=str(model_dir_abs) if model_dir_abs else None
        )
        audio_path = voice_client.synthesize(reply_text, audio_filename)

        # 3. Avatar Driving (Optional)
        video_path = None
        if generate_video:
            video_filename = f"outputs/video_{character_id}_{timestamp}.mp4"
            driver = AvatarDriver(api_url=char_conf.get("liveportrait_api_url"))
            video_path = driver.drive(
                image_path=char_conf.get("avatar_image", ""),
                audio_path=audio_path,
                output_path=video_filename
            )

        return {
            "reply_text": reply_text,
            "audio_path": audio_path if os.path.exists(audio_path) else None,
            "video_path": video_path if video_path and os.path.exists(video_path) else None
        }
