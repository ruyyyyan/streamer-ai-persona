import os
import json
from pathlib import Path
from typing import List, Dict, Optional


class PersonaAgent:
    """
    Manages conversational turns with a specific streamer persona
    using an OpenAI-compatible API interface with In-Context Few-Shot Learning.
    """

    def __init__(
        self,
        system_prompt: str,
        character_id: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        self.system_prompt = system_prompt
        self.character_id = character_id
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model_name = model_name or os.getenv("OPENAI_MODEL_NAME", "gemini-3.1-flash-lite")
        self.base_dir = Path(__file__).resolve().parent.parent.parent

        self.few_shots: List[Dict[str, str]] = []
        if self.character_id:
            corpus_file = self.base_dir / "data" / "corpus" / f"{self.character_id}_corpus.json"
            if corpus_file.exists():
                try:
                    with open(corpus_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.few_shots = data.get("dialogue_samples", [])
                except Exception as e:
                    print(f"[PersonaAgent] 加载 {self.character_id} 语料库失败: {e}")

        self.client = None
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            except ImportError:
                print("[PersonaAgent] openai 模块未安装，将使用离线模拟模式。")

    def chat(self, user_message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]

        # Inject 2-3 authentic few-shot dialogue samples to lock persona and speech mannerisms
        if self.few_shots:
            selected_shots = self.few_shots[:3]
            for shot in selected_shots:
                messages.append({"role": "user", "content": shot["user"]})
                messages.append({"role": "assistant", "content": shot["assistant"]})

        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        if not self.client:
            # Fallback mock reply if no API key is set
            return f"【本地离线模拟】主播收到了你的弹幕：“{user_message}”。（提示：配置 OPENAI_API_KEY 后可体验完整的大模型生成）"

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.85,
                max_tokens=220,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[生成出错: {str(e)}]"
