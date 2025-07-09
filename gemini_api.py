import google.generativeai as genai
import json
from typing import List, Dict
# gemini_api.py

# ✅ Gemini API Configuration
genai.configure(api_key="AIzaSyB5fFY--i-HVfmAP9lsr3csuzfV5NjZfYo")

# ✅ استخدم نموذج موجود فعليًا في حسابك (سريع وجيد)
MODEL_NAME = "models/gemini-2.5-flash"
model = genai.GenerativeModel(model_name=MODEL_NAME)

# ✅ Create a chat session once (to maintain history)
chat_session = model.start_chat(history=[])

# ✅ Chat function with optional history
def chat_with_gemeni(prompt, history=None):
    try:
        # Add user prompt to chat
        response = chat_session.send_message(prompt)
        
        # Return reply and current conversation history
        return response.text, chat_session.history

    except Exception as e:
        return f"⚠️ Gemini API error: {e}", []
    
# gemini_api.py أو الملف اللي فيه الدالة

## ✅ الحل النهائي المقترح لدالتك `generate_presentation_sections`:

def generate_presentation_sections(text: str, language: str = "english", max_slides: int = 20) -> List[Dict]:
    prompt = f"""
You are an expert at creating structured PowerPoint presentations.

Given the following content in {language}, generate a JSON object in the following format:
{{
  "slides": [
    {{
      "title": "Slide Title",
      "bullets": ["Bullet point 1", "Bullet point 2", "Bullet point 3"]
    }},
    ...
  ]
}}

Rules:
- Provide 3 to 5 bullet points per slide.
- Do not return anything outside the JSON object.
- Use easy language and summarize long parts into bullet points.

Content:
{text}
    """

    try:
        reply, _ = chat_with_gemeni(prompt)

        if not reply or not reply.strip():
            return [{"title": "Error", "bullets": ["Gemini returned empty response."]}]

        cleaned_reply = reply.strip()
        if cleaned_reply.startswith("```json"):
            cleaned_reply = cleaned_reply.replace("```json", "").strip()
        if cleaned_reply.startswith("```"):
            cleaned_reply = cleaned_reply[3:].strip()
        if cleaned_reply.endswith("```"):
            cleaned_reply = cleaned_reply[:-3].strip()

        data = json.loads(cleaned_reply)
        slides = data.get("slides", [])

        valid_slides = []
        for slide in slides:
            if isinstance(slide, dict) and "title" in slide and "bullets" in slide:
                valid_slides.append({
                    "title": str(slide["title"]).strip(),
                    "bullets": [str(b).strip() for b in slide["bullets"] if b]
                })

        return valid_slides[:max_slides]

    except json.JSONDecodeError as e:
        return [{"title": "Error", "bullets": [f"Invalid JSON response: {str(e)}"]}]
    except Exception as e:
        return [{"title": "Error", "bullets": [f"Failed to generate slides: {str(e)}"]}]
