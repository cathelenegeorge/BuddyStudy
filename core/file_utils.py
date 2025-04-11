import pdfplumber
import docx2txt
import tempfile
import os

def extract_text(file):
    ext = os.path.splitext(file.name)[1].lower()
    text = ""
    if ext == ".pdf":
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    elif ext == ".docx":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file.read())
            tmp.seek(0)
            text = docx2txt.process(tmp.name)
            os.unlink(tmp.name)
    return text
