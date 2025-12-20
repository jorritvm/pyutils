import pytest
from datetime import date, timezone
from pyutils.clock import parse_iso_date
from pyutils import clock

def test_extract_iso_date_found():
    text = "The date is 2024-06-15 in this string."
    assert clock.extract_iso_date(text) == "2024-06-15"

def test_extract_iso_date_not_found():
    text = "No date here!"
    assert clock.extract_iso_date(text) is None

def test_extract_iso_date_custom_pattern():
    text = "Date: 15/06/2024"
    pattern = r'\d{2}/\d{2}/\d{4}'
    assert clock.extract_iso_date(text, pattern) == "15/06/2024"

def test_get_current_date_str_format():
    fmt = "%Y-%m-%d"
    result = clock.get_current_date_str(fmt)
    assert isinstance(result, str)
    assert len(result) == 10  # e.g., "2024-06-15"

def test_get_current_time_str_format():
    fmt = "%H:%M:%S"
    result = clock.get_current_time_str(fmt)
    assert isinstance(result, str)
    assert len(result) == 8  # e.g., "12:34:56"

def test_get_current_date_and_time_str():
    date_fmt = "%Y-%m-%d"
    time_fmt = "%H:%M:%S"
    date_str, time_str = clock.get_current_date_and_time_str(date_fmt, time_fmt)
    assert isinstance(date_str, str)
    assert isinstance(time_str, str)
    assert len(date_str) == 10
    assert len(time_str) == 8

def test_parse_iso_date_valid():
    assert parse_iso_date("2024-06-15") == date(2024, 6, 15)
    assert parse_iso_date("1999-12-31") == date(1999, 12, 31)
    assert parse_iso_date("2024-6-5") == date(2024, 6, 5)

def test_parse_iso_date_invalid_format():
    with pytest.raises(ValueError):
        parse_iso_date("2024/06/15")
    with pytest.raises(ValueError):
        parse_iso_date("15-06-2024")
    with pytest.raises(ValueError):
        parse_iso_date("June 15, 2024")
    with pytest.raises(ValueError):
        parse_iso_date("")

def test_parse_iso_date_non_numeric():
    with pytest.raises(ValueError):
        parse_iso_date("abcd-ef-gh")
    with pytest.raises(ValueError):
        parse_iso_date("2024-xx-15")

def test_parse_iso_date_none():
    with pytest.raises(TypeError):
        parse_iso_date(None)
