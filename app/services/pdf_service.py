from io import BytesIO
from pdfminer.high_level import extract_text

def extract_text_from_pdf(raw_bytes: bytes) -> str:
    try:
        return (extract_text(BytesIO(raw_bytes)) or "").strip()
    except Exception as e:
        print("[pdf_service] error:", e)
        return ""
