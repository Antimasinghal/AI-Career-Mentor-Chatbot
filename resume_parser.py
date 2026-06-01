import io
import PyPDF2

def extract_text_from_pdf(pdf_bytes):
    """
    Extracts text content from a PDF file provided as bytes.
    """
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")

def extract_text_from_txt(txt_bytes):
    """
    Extracts text content from a text file provided as bytes.
    """
    try:
        return txt_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return txt_bytes.decode("latin1")
        except Exception as e:
            raise ValueError(f"Failed to parse Text file: {str(e)}")

def parse_resume(file_bytes, filename):
    """
    Parses a resume file based on extension and extracts text.
    """
    if not file_bytes:
        return ""
        
    lower_filename = filename.lower()
    if lower_filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif lower_filename.endswith(".txt"):
        return extract_text_from_txt(file_bytes)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or TXT file.")
