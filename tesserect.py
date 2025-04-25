import pytesseract

# For Windows: Set the Tesseract path manually
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Test if it's working
print(pytesseract.get_tesseract_version())
