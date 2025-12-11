import pytest
from datetime import timezone
from pyutils import time

def test_extract_iso_date_found():
    text = "The date is 2024-06-15 in this string."
    assert time.extract_iso_date(text) == "2024-06-15"

def test_extract_iso_date_not_found():
    text = "No date here!"
    assert time.extract_iso_date(text) is None

def test_extract_iso_date_custom_pattern():
    text = "Date: 15/06/2024"
    pattern = r'\d{2}/\d{2}/\d{4}'
    assert time.extract_iso_date(text, pattern) == "15/06/2024"

def test_get_current_date_str_format():
    fmt = "%Y-%m-%d"
    result = time.get_current_date_str(fmt)
    assert isinstance(result, str)
    assert len(result) == 10  # e.g., "2024-06-15"

def test_get_current_time_str_format():
    fmt = "%H:%M:%S"
    result = time.get_current_time_str(fmt)
    assert isinstance(result, str)
    assert len(result) == 8  # e.g., "12:34:56"

def test_get_current_date_and_time_str():
    date_fmt = "%Y-%m-%d"
    time_fmt = "%H:%M:%S"
    date_str, time_str = time.get_current_date_and_time_str(date_fmt, time_fmt)
    assert isinstance(date_str, str)
    assert isinstance(time_str, str)
    assert len(date_str) == 10
    assert len(time_str) == 8
