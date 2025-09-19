import PyPDF2
from pathlib import Path

pdf_path = Path.home() / "Desktop" / "Reasearch_paper.pdf"

with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
print(text)