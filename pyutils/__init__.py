from .dicts import merge_dicts, has_empty_leaves
from .time import extract_iso_date, get_current_date_and_time_str, get_current_date_str, get_current_time_str

__all__ = [
    "merge_dicts",
    "has_empty_leaves",
    "extract_iso_date",
    "get_current_date_and_time_str",
    "get_current_date_str",
    "get_current_time_str",
    "test"
]


def test():
    print("test")
