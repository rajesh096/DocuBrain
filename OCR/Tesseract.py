import pytesseract
from PIL import Image

# Set path to Tesseract executable (only needed for Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load the image
image_path = "E:\Project\DocuBrain\Invoice_samples\invoice4.webp"  # Change this to your image path
image = Image.open(image_path)

# Perform OCR
text = pytesseract.image_to_string(image)

# Print extracted text
print(text)
