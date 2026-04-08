import os
import gradio as gr
from groq import Groq

# 1. Fetch the key from Hugging Face Secrets (Looking for 'Alexa')
api_key = os.environ.get("Alexa")

# 2. Initialize the Groq client safely
client = None
if api_key:
    client = Groq(api_key=api_key)

# 3. The AI generation logic
def generate_linkedin_post(topic, tone, key_points):
    if not api_key:
        return "❌ Error: Secret named 'Alexa' not found in Hugging Face Settings."
    if not client:
        return "❌ Error: Groq client failed to initialize."

    system_prompt = (
        "You are a world-class LinkedIn Content Strategist. Your goal is to write posts that "
        "stop the scroll. Use a strong hook, plenty of white space, relevant emojis, "
        "and 3-5 trending hashtags."
    )
    
    user_prompt = f"Topic: {topic}\nTone: {tone}\nKey Points: {key_points}\n\nWrite a viral LinkedIn post."
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7, 
            max_tokens=1000,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# 4. CUSTOM STYLING (CSS)
custom_css = """
.gradio-container {
    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important;
}
#main-container {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
#gen-button {
    background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%) !important;
    color: white !important;
    font-weight: bold !important;
}
"""

# 5. Build the Interface
with gr.Blocks() as app:
    with gr.Column(elem_id="main-container"):
        gr.Markdown("<h1 style='text-align: center; color: #1a2a6c;'>🚀 Viral LinkedIn Architect</h1>")
        
        with gr.Row():
            with gr.Column():
                topic_input = gr.Textbox(label="🎯 Topic", placeholder="e.g., The future of AI")
                tone_input = gr.Dropdown(
                    choices=["Professional", "Storytelling", "Inspirational", "Educational", "Witty"], 
                    label="🎭 Tone", 
                    value="Professional"
                )
                points_input = gr.Textbox(label="💡 Key Details", placeholder="Stats or points...", lines=3)
                generate_btn = gr.Button("GENERATE POST ✨", elem_id="gen-button")
            
            with gr.Column():
                # Using gr.Code because it has a native, stable copy button in all Gradio versions
                output_text = gr.Code(
                    label="📱 Your Ready-to-Post Content", 
                    language="markdown",
                    interactive=False
                )
                gr.Markdown("Click the **copy icon** in the top right of the black box above.")
        
    generate_btn.click(
        fn=generate_linkedin_post,
        inputs=[topic_input, tone_input, points_input],
        outputs=output_text
    )

# 6. Launch
if __name__ == "__main__":
    app.launch(css=custom_css, theme=gr.themes.Soft())
