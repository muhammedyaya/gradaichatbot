from gtts import gTTS
import os
import tempfile
import platform

def speak(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang)

        # Create and close a temp file before playing
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name

        # Save the audio
        tts.save(temp_path)

        # Play the file depending on the OS
        if platform.system() == "Windows":
            os.system(f'start /min "" "{temp_path}"')
        elif platform.system() == "Darwin":
            os.system(f"afplay '{temp_path}'")
        else:
            os.system(f"xdg-open '{temp_path}'")

    except Exception as e:
        print(f"TTS Error: {e}")
