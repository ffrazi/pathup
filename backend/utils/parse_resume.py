import pdfplumber
import docx2txt
import pytesseract
from PIL import Image

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return '\n'.join(page.extract_text() or '' for page in pdf.pages)
    except Exception as e:
        print(f"[WARN] PDF extraction failed: {e}")
        return ""

def extract_text_from_docx(docx_path):
    """Extract text from DOCX using docx2txt."""
    try:
        return docx2txt.process(docx_path)
    except Exception as e:
        print(f"[WARN] DOCX extraction failed: {e}")
        return ""

def extract_text_from_image(image_path):
    """Extract text from image using pytesseract."""
    try:
        img = Image.open(image_path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        print(f"[WARN] Image OCR failed: {e}")
        return ""

def extract_resume_text(file_path):
    """
    Extract text from a resume file of any supported type.
    Supports PDF, DOCX, images, and plain text.
    """
    file_lower = file_path.lower()

    if file_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_lower.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_lower.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        return extract_text_from_image(file_path)
    else:
        # ✅ Robust fallback for plain text files
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            try:
                return raw_data.decode('utf-8')
            except UnicodeDecodeError:
                # fallback for non-UTF8 text (Windows, Latin1, etc.)
                return raw_data.decode('latin1', errors='ignore')
        except Exception as e:
            print(f"[WARN] Text file extraction failed: {e}")
            return ""