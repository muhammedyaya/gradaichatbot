import streamlit as st
from io import BytesIO
import traceback
import os
import json
from PIL import Image

from file_handler import load_file
from gemini_api import chat_with_gemeni, generate_presentation_sections
from tts import speak
from image_gen import generate_image_with_stability
from presentation import create_presentation
from ocr_handler import ocr_space_file

# --- إعداد الصفحة ---
st.set_page_config(page_title="Smart AI Chatbot", layout="wide")
st.title("🤖 Smart AI Chatbot Assistant")

# --- تهيئة الجلسة ---
def init_session():
    defaults = {
        "chat_history": [],
        "file_text": "",
        "select_template": False,
        "slides_to_generate": [],
        "template_selected": None,
        "pptx_bytes": None,
        "show_download_button": False,
        "show_image_form": False,
        "generated_image": None,
        "clear_chat_trigger": False,
        "session_loaded": False,
        "image_prompt_from_bot": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# --- الشريط الجانبي: إدارة الجلسة ---
with st.sidebar:
    st.markdown("### 💾 Session Management")
    if st.button("💾 Save Session"):
        session_data = {
           "chat_history": [
                (role, msg.decode("utf-8") if isinstance(msg, bytes) else msg)
                for role, msg in st.session_state.chat_history
                if not isinstance(msg, bytes)
            ],    
            "file_text": st.session_state.file_text,
            "slides_to_generate": st.session_state.slides_to_generate,
            "template_selected": st.session_state.template_selected,
        }
        json_bytes = json.dumps(session_data).encode("utf-8")
        st.download_button("⬇️ Download Session", data=json_bytes, file_name="session.json", mime="application/json")

    uploaded_session = st.file_uploader("📤 Load Session", type=["json"], label_visibility="collapsed")
    if uploaded_session and not st.session_state.session_loaded:
        loaded = json.load(uploaded_session)
        st.session_state.chat_history = loaded.get("chat_history", [])
        st.session_state.file_text = loaded.get("file_text", "")
        st.session_state.slides_to_generate = loaded.get("slides_to_generate", [])
        st.session_state.template_selected = loaded.get("template_selected", None)
        st.session_state.session_loaded = True
        st.success("✅ Session loaded successfully.")

# --- التابات ---
tabs = st.tabs(["📁 File & Chat", "🎯 Smart Actions", "🎞️ Presentation"])

# --- تاب 1: الملف والدردشة ---
with tabs[0]:
    uploaded_file = st.file_uploader("📂 Upload a .pdf, .txt, or image file", type=["pdf", "txt", "png", "jpg", "jpeg"])
    if uploaded_file:
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        try:
            used_ocr = False
            if uploaded_file.type in ["application/pdf", "text/plain"]:
                text, used_ocr = load_file(file_path)
            else:
                st.image(uploaded_file, caption="📷 Uploaded Image Preview", use_container_width=True)
                text = ocr_space_file(file_path)
                used_ocr = True
            st.session_state.file_text = text
            with st.expander("📄 Preview File Content"):
                st.text_area("File Content", value=text, height=200)
            if used_ocr:
                st.info("🧠 OCR was used.")
                if len(text.strip()) < 30:
                    st.warning("⚠️ Very little text was extracted.")
        except Exception as e:
            st.error(f"❌ Failed to read file: {e}\n{traceback.format_exc()}")

    st.subheader("💬 Ask a Question")
    user_input = st.text_input("Type your question:")
    if st.button("🔍 Ask") and user_input:
        with st.spinner("🤖 Thinking..."):
            try:
                prompt = st.session_state.file_text + "\n\n" + user_input if st.session_state.file_text else user_input
                reply, _ = chat_with_gemeni(prompt)
                st.session_state.chat_history.extend([
                    ("👤 You", user_input),
                    ("🤖 Bot", reply),
                ])
                st.session_state.image_prompt_from_bot = reply
            except Exception as e:
                st.error(f"⚠️ Error: {e}\n{traceback.format_exc()}")

# --- تاب 2: الإجراءات الذكية ---
with tabs[1]:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Summarize Document"):
            with st.spinner("Summarizing..."):
                reply, _ = chat_with_gemeni("Summarize this nicely:\n" + st.session_state.file_text)
                st.session_state.chat_history.append(("🤖 Summary", reply))
                st.session_state.image_prompt_from_bot = reply

        if st.button("📝 Generate Quiz"):
            with st.spinner("Generating quiz..."):
                reply, _ = chat_with_gemeni("Create 5 MCQs with answers:\n" + st.session_state.file_text)
                st.session_state.chat_history.append(("🤖 Quiz", reply))

    with col2:
        if st.button("💡 Create Flashcards"):
            with st.spinner("Creating flashcards..."):
                reply, _ = chat_with_gemeni("Create flashcards:\n" + st.session_state.file_text)
                st.session_state.chat_history.append(("🤖 Flashcards", reply))

        if st.button("📚 Extract Notes"):
            with st.spinner("Extracting notes..."):
                reply, _ = chat_with_gemeni("Extract key points:\n" + st.session_state.file_text)
                st.session_state.chat_history.append(("🤖 Notes", reply))
                st.session_state.image_prompt_from_bot = reply

    if st.button("🔍 Explain Concepts"):
        with st.spinner("Explaining..."):
            reply, _ = chat_with_gemeni("Explain concepts:\n" + st.session_state.file_text)
            st.session_state.chat_history.append(("🤖 Explanation", reply))
            st.session_state.image_prompt_from_bot = reply

    if st.button("🎨 Generate Image from Last Bot Reply"):
        prompt = st.session_state.image_prompt_from_bot
        if prompt:
            with st.spinner("Generating image..."):
                try:
                    image_data = generate_image_with_stability(prompt)
                    if image_data:
                        image_data.seek(0)
                        image_bytes = image_data.getvalue()
                        st.image(image_data, caption="🖼️ Generated Image", use_container_width=True)
                        st.session_state.generated_image = image_data
                        st.session_state.chat_history.append(("🖼️ Image from Bot", image_bytes))
                except Exception as e:
                    st.error(f"❌ Failed to generate image: {str(e)}")
        else:
            st.warning("⚠️ No recent bot reply to use as prompt.")

# --- تاب 3: توليد العرض التقديمي ---
with tabs[2]:
    if st.button("🎞️ Generate Presentation"):
        with st.spinner("🛠️ Analyzing content and generating slides..."):
            try:
                slides = generate_presentation_sections(
                    text=st.session_state.file_text,
                    max_slides=10,
                    language="english"
                )
                st.session_state.slides_to_generate = slides
                st.session_state.select_template = True
                st.success("✅ Slide structure generated.")
            except Exception as e:
                st.error(f"❌ {e}\n{traceback.format_exc()}")

    for i, slide in enumerate(st.session_state.slides_to_generate):
        with st.expander(f"Slide {i+1}: {slide['title']}"):
            for bullet in slide['bullets']:
                st.markdown(f"- {bullet}")
            if st.button(f"🖼️ Generate Image from Slide {i+1}",key=f"generate_img_slide_{i}"):
                full_slide_text = slide["title"] + "\n" + "\n".join(slide["bullets"])
                with st.spinner("Creating image..."):
                    try:
                        image_data = generate_image_with_stability(full_slide_text)
                        if image_data:
                            image_data.seek(0)
                            image_bytes = image_data.getvalue()
                            st.image(image_data, caption=f"🖼️ Image for Slide {i+1}", use_container_width=True)
                            buffer = BytesIO(image_bytes)
                            buffer.seek(0)
                            st.download_button(
                                label=f"📥 Download Slide {i+1} Image",
                                data=buffer,
                                file_name=f"slide_{i+1}_image.png",
                                mime="image/png",
                                key=f"download_slide_{i}"


                                             )
                            st.session_state.chat_history.append((f"🖼️ Slide {i+1} Image", image_bytes))
                    except Exception as e:
                        st.error(f"❌ Image generation failed: {str(e)}")

    if st.session_state.select_template:
        st.markdown("## 🎨 Select a Presentation Template")
        template_options = {
            "Professional": "templates/professional.pptx",
            "Creative": "templates/creative.pptx",
            "Minimalist": "templates/minimalist.pptx",
            "Futuristic": "templates/futuristic.pptx",
        }
        template_previews = {
        "Professional": "static/thumbnails/professional.jpg",
        "Creative": "static/thumbnails/creative.jpg",
        "Minimalist": "static/thumbnails/minimalist.jpg",
        "Futuristic": "static/thumbnails/futuristic.jpg",
        }
        selected_template = st.radio(
            "Choose template:",
            list(template_options.keys()),
            horizontal=True,
            key="template_selection_radio"
        )
            # 🔍 Show preview image of the selected template
        cols = st.columns(len(template_options))
        for idx, (template_name, preview_path) in enumerate(template_previews.items()):
            with cols[idx]:
                if os.path.exists(preview_path):
                    st.image(preview_path, caption=template_name, use_container_width=True)
                else:
                    st.warning(f"No preview for {template_name}")

        if st.button("🔘 Use Template"):
            st.session_state.template_selected = template_options[selected_template]
            st.session_state.show_download_button = True
            st.success(f"✅ Template selected: {selected_template}")

    if st.session_state.show_download_button and st.session_state.template_selected:
        with st.spinner("💾 Generating Presentation..."):
            pptx_bytes = create_presentation(
                st.session_state.slides_to_generate,
                template_path=st.session_state.template_selected
            )
            st.download_button(
                label="📥 Download PowerPoint",
                data=pptx_bytes,
                file_name="smart_presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

# --- شات دائم أسفل الصفحة ---
st.markdown("---")
st.markdown("### 🕓 Chat History")
if st.session_state.clear_chat_trigger:
    st.session_state.chat_history = []
    st.session_state.clear_chat_trigger = False

for role, msg in st.session_state.chat_history:
    st.markdown(f"**{role}:**")
    if isinstance(msg, bytes):
        st.image(msg, use_container_width=True)
        img = Image.open(BytesIO(msg))
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        st.download_button(
            label="📥 Download Image",
            data=buffer,
            file_name="chat_image.png",
            mime="image/png",
            key=f"download_chat_img_{id(buffer)}"
                  )
    else:
        st.markdown(msg)
if st.button("🗑️ Clear Chat History"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("✅ All session data cleared.")
    st.rerun()
