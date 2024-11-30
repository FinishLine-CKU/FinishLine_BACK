import PyPDF2

def extract_text_from_pdf(pdf_file):
    """
    PDF 파일에서 텍스트를 추출하는 헬퍼 함수.
    Args:
        pdf_file: 업로드된 PDF 파일 객체
    Returns:
        str: 추출된 텍스트
    """
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
