from io import BytesIO


def extract_text(content: bytes, filename: str) -> str:
    suffix = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if suffix == "pdf":
        import fitz
        document = fitz.open(stream=content, filetype="pdf")
        return "\n".join(page.get_text() for page in document).strip()
    if suffix == "docx":
        from docx import Document
        return "\n".join(paragraph.text for paragraph in Document(BytesIO(content)).paragraphs).strip()
    raise ValueError("Only PDF and DOCX files are supported.")
