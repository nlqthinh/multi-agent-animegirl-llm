import gradio as gr
from chat import chat_respond

LOG_LEVEL = "INFO"


def chat_logic(message, chat_history):
    # 1) The user message + "Waiting..." placeholder
    # chat_history.append([message, "Waiting..."])
    yield "", chat_history

    # 2) Bot responds
    updated_chat_history = chat_respond(message, chat_history)
    
    # Overwrite local chat_history with the updated one
    chat_history[:] = updated_chat_history
    yield "", chat_history


with gr.Blocks() as demo:
    gr.Markdown("# Ask Seika Ijichi anything using Gradio and Multi Agent")

    chatbot = gr.Chatbot(
        label="Seika-chan",
        height=1000,
        avatar_images=["images/bocchi.png", "images/Seika.png"],
    )

    message = gr.Textbox(
        label="Message",
        placeholder="Enter your message and press Enter...",
        show_label=False,
    )

    # The function chat_logic is called on user submit
    # The inputs are [message, chatbot] and outputs are [message, chatbot]
    message.submit(chat_logic, [message, chatbot], [message, chatbot])

if __name__ == "__main__":
    demo.launch()