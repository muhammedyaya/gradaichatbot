# gradaichatbot


# 🤖 Smart AI Chatbot Assistant (Streamlit App)

This is a powerful and interactive **AI-powered Streamlit application** that allows users to analyze files, generate presentations, create quizzes, extract notes, and generate AI images using Gemini and Stability APIs.

## 🚀 Features

- 📁 Upload files (PDF, TXT, Images)
- 🧠 Extract text via OCR or directly
- 💬 Ask contextual questions using Gemini
- 🧾 Summarize, quiz, flashcards, note extraction
- 🖼️ AI image generation (Stability AI)
- 🎞️ Automatic presentation generation with slide preview
- 🎨 Multiple presentation templates with preview
- 📥 Download presentation as `.pptx`
- 💾 Save/load session with history and file state
- 🗑️ Clear session and chat with one click

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/)
- Python 3.10+
- Google Gemini API
- Stability AI API
- OCR.space API
- `python-pptx`, `Pillow`, `json`, `io`, `os`

## 📂 Project Structure

```

.
├── app.py                     # Main Streamlit app
├── gemini\_api.py              # Handles communication with Gemini
├── image\_gen.py               # Generates images via Stability API
├── presentation.py            # Creates PowerPoint presentation
├── ocr\_handler.py             # OCR processing via OCR.space
├── templates/                 # PowerPoint template files (.pptx)
├── static/
│   └── thumbnails/            # Template preview images (.jpg)
└── file\_handler.py            # File reading and text extraction

````

## ▶️ How to Run

1. Clone the repository:

```bash
git clone https://github.com/your-username/smart-ai-chatbot.git
cd smart-ai-chatbot
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your API keys in `.env` or directly in the script:

* `GEMINI_API_KEY`
* `STABILITY_API_KEY`
* `OCR_API_KEY`

4. Run the app:

```bash
streamlit run app.py
```

## 👥 Contributors

* **Mohamed Osama Saad Hamed**
* **Mohammed Yahya Mohammed Saaid**

## 📄 License

MIT License

---

Built with ❤️ using Streamlit and powerful AI APIs.

```

---

```
