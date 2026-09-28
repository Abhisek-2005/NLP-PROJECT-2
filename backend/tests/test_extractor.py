import pytest
from pathlib import Path
from backend.app.services.extractor import DocumentExtractorService

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_data"

def test_extract_txt():
    txt_path = SAMPLE_DIR / "sample_resume_devops.txt"
    assert txt_path.exists(), "Sample text resume file should exist"
    content = txt_path.read_bytes()
    text = DocumentExtractorService.extract(txt_path.name, content)
    assert len(text) > 100
    assert "SAMIRA KHAN" in text
    assert "Kubernetes" in text

def test_extract_pdf():
    pdf_path = SAMPLE_DIR / "sample_resume_ml_nlp_engineer.pdf"
    assert pdf_path.exists(), "Sample PDF resume file should exist"
    content = pdf_path.read_bytes()
    text = DocumentExtractorService.extract(pdf_path.name, content)
    assert len(text) > 100
    assert "ALEX MORGAN" in text
    assert "PyTorch" in text or "Machine Learning" in text

def test_extract_docx():
    docx_path = SAMPLE_DIR / "sample_resume_full_stack.docx"
    assert docx_path.exists(), "Sample DOCX resume file should exist"
    content = docx_path.read_bytes()
    text = DocumentExtractorService.extract(docx_path.name, content)
    assert len(text) > 100
    assert "JORDAN REED" in text
    assert "React" in text
