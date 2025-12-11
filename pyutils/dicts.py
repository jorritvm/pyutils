__all__ = ["merge_dicts", "has_empty_leaves"]

def merge_dicts(insert_into: dict, insert_from: dict) -> dict: 
    """Recursively merge dict2 into dict1. Values in dict2 overwrite those in dict1."""
    for key, value in insert_from.items():
        if isinstance(value, dict) and key in insert_into and isinstance(insert_into[key], dict):
            # If both values are dictionaries, merge them recursively
            merge_dicts(insert_into[key], value)
        else:
            # Otherwise, overwrite the value in dict1 with the value from dict2
            insert_into[key] = value
    return insert_into


def has_empty_leaves(d: dict) -> bool:
    """Recursively checks if any leaf value in a nested dictionary is None or an empty string."""
    for key, value in d.items():
        if isinstance(value, dict):
            # Recurse into nested dictionaries
            if has_empty_leaves(value):
                return True
        elif value is None or value == "":
            return True
    return False