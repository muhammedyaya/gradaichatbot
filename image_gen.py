from io import BytesIO
import requests
import os
from dotenv import load_dotenv     
# Load environment variables from .env file
load_dotenv(dotenv_path=".env")
def generate_image_with_stability(prompt):


    try:
        url = "https://api.stability.ai/v2beta/stable-image/generate/core"
        headers = {
            "Authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",
            "Accept": "image/*"
        }
        files = {
            "prompt": (None, prompt),
            "output_format": (None, "png"),
            "aspect_ratio": (None, "1:1"),
            "style_preset": (None, "digital-art")
        }

        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            return BytesIO(response.content)  # ← wrap in BytesIO
        else:
            print("❌ API error:", response.status_code, response.text)
            return None
    except Exception as e:
        print("❌ Exception:", e)
        return None
