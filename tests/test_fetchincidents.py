import pytest
import urllib.request
from unittest.mock import patch, MagicMock
from fetchincidents import fetchincidents  # Import fetchincidents from your actual module


# Mock the urlopen function
@patch('urllib.request.urlopen')
def test_fetchincidents(mock_urlopen):
    # Set up the mock response
    mock_response = MagicMock()
    mock_response.read.return_value = b"mocked data"
    
    # Assign the mock response to urlopen
    mock_urlopen.return_value = mock_response
    
    # URL to be used in the test (it can be anything since it's mocked)
    test_url = "http://example.com/incidents"
    
    # Call the function
    result = fetchincidents(test_url)
    
    # Check that urlopen was called with the correct arguments
    mock_urlopen.assert_called_once()
    
    # Assert the function's result is what we expect
    assert result == b"mocked data"

# test_fetchincidents()