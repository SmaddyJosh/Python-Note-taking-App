import pytesseract
from PIL import Image
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Load an image of handwritten text
image = Image.open("journey.jpg")

# Convert image to text
text = pytesseract.image_to_string(image)

print("Recognized Text:", text)
