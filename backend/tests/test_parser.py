import pytest
from app.resume_parser import extract_text


def test_rejects_unknown_file_type():
    with pytest.raises(ValueError):
        extract_text(b"hello", "resume.txt")
