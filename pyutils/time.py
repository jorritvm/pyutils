from datetime import datetime, timezone
import re

__all__ = [
    "extract_iso_date",
    "get_current_date_and_time_str",
    "get_current_date_str",
    "get_current_time_str",
]

def extract_iso_date(text: str, pattern: str = r'\d{4}-\d{2}-\d{2}') -> str | None:
    # define iso date pattern
    iso_date_pattern = re.compile(pattern)
    # Define the regular expression to match the ISO date
    match = re.search(iso_date_pattern, text)
    # Check if match is found and return the matched string
    if match:
        return match.group(0)
    # Return None if no match is found
    return None

def get_current_date_and_time_str(date_format: str,
                                  time_format: str,
                                  tz: timezone = timezone.utc) -> tuple[str, str]:
    """Return the current date and time as a tuple of strings formatted as desired."""
    return (get_current_date_str(date_format, tz), get_current_time_str(time_format, tz))

def get_current_date_str(date_format: str,
                         tz: timezone = timezone.utc) -> str:
    """Return the current date as a string formatted as desired."""
    now_datetime = datetime.now(tz)
    return now_datetime.strftime(date_format)

def get_current_time_str(time_format: str,
                         tz: timezone = timezone.utc) -> str:
    """Return the current time as a string formatted as desired."""
    now_datetime = datetime.now(tz)
    return now_datetime.strftime(time_format)
