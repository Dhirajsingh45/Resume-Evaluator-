from services.pdf_services import extract_text_from_pdf
from services.ocr_services import extract_text_from_image


def extract_text(file):

    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif filename.endswith((".jpg", ".jpeg", ".png")):
        return extract_text_from_image(file)

    else:
        raise ValueError("Unsupported file type")