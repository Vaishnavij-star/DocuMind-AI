from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Set path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Convert PDF to images
pages = convert_from_path("1,0-KNN+Classification+And+Regression.pdf")  # Make sure PDF is in the same folder

# Extract text from each page
for i, page in enumerate(pages):
    text = pytesseract.image_to_string(page)
    print(f"--- Page {i+1} ---")
    print(text)
    print("\n")
