# ocr_handler.py
import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")
api_key = os.getenv("API_KEY_OCR") or "helloworld"
def ocr_space_file(filename, language='eng', max_retries=3, delay=3):
    """OCR.space API call with retries and fallback"""

    payload = {
        'isOverlayRequired': False,
        'apikey': api_key,
        'language': language,
    }

    for attempt in range(1, max_retries + 1):
        try:
            with open(filename, 'rb') as f:
                print(f"📤 Attempt {attempt} sending to OCR.space...")
                r = requests.post(
                    'https://api.ocr.space/parse/image',
                    files={'filename': f},
                    data=payload,
                    timeout=30  # Increased timeout for larger files
                )

            result = r.json()

            if result.get("IsErroredOnProcessing"):
                raise Exception(result.get("ErrorMessage", ["Unknown Error"])[0])

            print("✅ OCR success")
            return result["ParsedResults"][0]["ParsedText"]

        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                print(f"⏳ Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("❌ All OCR attempts failed. Using fallback.")

    return "Dummy text from fallback (helloworld)"
