import pytest
from pyutils.dicts import merge_dicts, has_empty_leaves

def test_merge_dicts():
    dict1 = {"a": 1, "b": {"c": 2}}
    dict2 = {"b": {"d": 3}, "e": 4}
    result = merge_dicts(dict1, dict2)
    expected = {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}
    assert result == expected

def test_has_empty_leaves():
    dict_with_empty = {"a": 1, "b": {"c": None}}
    dict_without_empty = {"a": 1, "b": {"c": 2}}
    assert has_empty_leaves(dict_with_empty) is True
    assert has_empty_leaves(dict_without_empty) is False