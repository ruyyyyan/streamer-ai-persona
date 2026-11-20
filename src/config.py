import os
from pathlib import Path
from typing import Dict, Any
import yaml


class ConfigLoader:
    def __init__(self, config_path: str = "configs/characters.yaml"):
        self.config_path = Path(config_path)
        self.base_dir = self.config_path.parent.parent

    def load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found at: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_character_config(self, character_id: str) -> Dict[str, Any]:
        config = self.load_config()
        characters = config.get("characters", {})
        if character_id not in characters:
            raise ValueError(f"Character '{character_id}' not found in configuration.")
        char_conf = characters[character_id]

        prompt_file = self.base_dir / char_conf.get("prompt_file", "")
        if prompt_file.exists():
            with open(prompt_file, "r", encoding="utf-8") as pf:
                char_conf["system_prompt"] = pf.read().strip()
        else:
            char_conf["system_prompt"] = "你是一个虚拟主播助手。"

        return char_conf
