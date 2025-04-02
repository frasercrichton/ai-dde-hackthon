import pdfplumber
import re

# pymupdf


class PDFPipeline:

    def __init__(self, pdf_path=None):
        self.pdf_path = pdf_path
        pass

    def get_pages(self, pdf_path):
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text())
        return pages

