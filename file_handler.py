# file_handler.py
import os
from ocr_handler import ocr_space_file
from pdf2image import convert_from_path
import tempfile
import fitz

def load_file(file_path):
    """
    Loads content from a .txt or .pdf file and returns (text, used_ocr).
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        return load_txt(file_path), False

    elif ext == ".pdf":
        return load_pdf(file_path)

    else:
        raise ValueError("Unsupported file format: Only .txt and .pdf are supported.")

def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def load_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        if text.strip():
            return text, False  # PDF عادي

        # OCR: PDF ممسوح ضوئيًا
        ocr_text = ""
        with tempfile.TemporaryDirectory() as temp_dir:
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                image_path = os.path.join(temp_dir, f"page_{i+1}.png")
                image.save(image_path, "PNG")
                page_text = ocr_space_file(image_path)
                ocr_text += f"\n\n--- Page {i+1} ---\n{page_text}"

        return ocr_text or "[No text found in scanned PDF]", True

    except Exception as e:
        raise ValueError(f"Error processing PDF file: {str(e)}")
