from pdf2image import convert_from_path

images = convert_from_path("temp_CSE425_ALL_Sheets.pdf")  # استبدل باسم ملف PDF
for i, img in enumerate(images):
    img.save(f"page_{i+1}.png", "PNG")