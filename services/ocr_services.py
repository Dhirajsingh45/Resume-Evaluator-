import io
import pytesseract
from PIL import Image

# Path to Tesseract on Windows
pytesseract.pytesseract.tesseract_cmd = (
    r"C:/Program Files/Tesseract-OCR/tesseract.exe"
)

def extract_text_from_image(file):
    image = Image.open(io.BytesIO(file.read()))

    text = pytesseract.image_to_string(image)

    return text