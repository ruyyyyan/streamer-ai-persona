import gradio as gr
from src.config import ConfigLoader
from src.pipeline import StreamerPipeline

pipeline = StreamerPipeline()
config_loader = ConfigLoader()
config = config_loader.load_config()
char_dict = {
    v.get("display_name", k): k
    for k, v in config.get("characters", {}).items()
}


def normalize_history(chat_history):
    clean = []
    if not chat_history:
        return clean
    for item in chat_history:
        if isinstance(item, dict) and "role" in item and "content" in item:
            clean.append(item)
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            u, b = item
            if u:
                clean.append({"role": "user", "content": str(u)})
            if b:
                clean.append({"role": "assistant", "content": str(b)})
    return clean


def respond(character_display: str, message: str, generate_video: bool, chat_history):
    chat_history = normalize_history(chat_history)
    if not message or not message.strip():
        return chat_history, None, None, ""

    char_id = char_dict.get(character_display, "xuanshen")
    result = pipeline.run(char_id, message, generate_video=generate_video)

    # Gradio 5/6+ requires messages format (list of dicts with role and content)
    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": result["reply_text"]})
    return chat_history, result["audio_path"], result["video_path"], ""


with gr.Blocks(title="AI 虚拟主播对话工作流") as demo:
    gr.Markdown("# 🎙️ AI 虚拟主播/数字人多模态交互工作流")
    gr.Markdown("开源模块化管线：LLM 人设对话 ➡️ 语音合成 (TTS) ➡️ 动态数字人面部驱动 (LivePortrait/SadTalker)")

    with gr.Row():
        with gr.Column(scale=4):
            char_selector = gr.Dropdown(
                choices=list(char_dict.keys()),
                value=list(char_dict.keys())[0] if char_dict else None,
                label="选择主播人设模板"
            )
            chatbot = gr.Chatbot(label="直播间弹幕互动", height=420)
            msg_input = gr.Textbox(label="发送弹幕", placeholder="在此输入弹幕内容，按回车发送...")
            with gr.Row():
                video_checkbox = gr.Checkbox(label="启用数字人面部动画驱动 (需本地启动渲染后端)", value=False)
                send_btn = gr.Button("发送", variant="primary")
                clear_btn = gr.ClearButton([msg_input, chatbot], value="清空对话")

        with gr.Column(scale=3):
            gr.Markdown("### 🔊 实时语音输出")
            audio_output = gr.Audio(label="合成语音", type="filepath")
            gr.Markdown("### 🎥 数字人视频输出")
            video_output = gr.Video(label="生成视频")

    send_btn.click(
        respond,
        inputs=[char_selector, msg_input, video_checkbox, chatbot],
        outputs=[chatbot, audio_output, video_output, msg_input]
    )
    msg_input.submit(
        respond,
        inputs=[char_selector, msg_input, video_checkbox, chatbot],
        outputs=[chatbot, audio_output, video_output, msg_input]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
