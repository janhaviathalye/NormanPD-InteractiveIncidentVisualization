import pytest
from unittest.mock import MagicMock, patch
from extractincidents import extractincidents  # Adjust this import according to your project structure
from io import BytesIO

def test_extract_incidents():

    with open('./docs/2024-12-04_daily_case_summary.pdf', 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
    
    total_records = extractincidents(pdf_bytes)

    assert len(total_records) == 37

# test_extract_incidents()