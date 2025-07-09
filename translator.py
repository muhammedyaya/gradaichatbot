# translator.py

from googletrans import Translator

translator = Translator()

def translate_text(text, dest="ar"):
    try:
        translated = translator.translate(text, dest=dest)
        return translated.text
    except Exception as e:
        return f"Translation error: {str(e)}"
