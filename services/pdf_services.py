import fitz #Extract text from the files 


def extract_text_from_pdf(file):
    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text