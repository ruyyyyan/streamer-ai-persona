import os
from typing import List, Dict, Optional
from openai import OpenAI


class PersonaAgent:
    """
    Manages conversational turns with a specific streamer persona
    using an OpenAI-compatible API interface (e.g. DeepSeek, Qwen, Ollama, OpenAI).
    """

    def __init__(
        self,
        system_prompt: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: str = "gpt-3.5-turbo"
    ):
        self.system_prompt = system_prompt
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model_name = model_name

        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat(self, user_message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        if not self.client:
            # Fallback mock reply if no API key is set, ensuring zero-error local smoke tests
            return f"【本地离线模拟】主播收到了你的弹幕：“{user_message}”。（提示：配置 OPENAI_API_KEY 后可体验完整的大模型生成）"

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.85,
                max_tokens=250,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[生成出错: {str(e)}]"
