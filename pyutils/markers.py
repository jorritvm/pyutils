import os
import inspect
import shutil

__all__ = [
    "title",
    "subtitle",
    "marker_line",
]

def title(title: str = None, min_width: int = 0) -> str:
    """Returns a title banner. If no title is provided, the caller's filename is used.
    Example output:
    ==============================
    ===         title          ===
    ==============================
    """
    if title is None:
        # Find the caller's file
        frame = inspect.stack()[1]
        caller_file = frame.filename
        title = os.path.basename(caller_file)

    banner_width = max(len(title) + 8, min_width)
    padding = banner_width - (len(title) + 8) + 2
    left_pad = padding // 2
    right_pad = padding - left_pad
    line = "=" * banner_width
    return f"\n{line}\n==={' ' * left_pad}{title}{' ' * right_pad}===\n{line}"

def subtitle(subtitle, min_width: int = 0) -> str:
    """Returns a subtitle banner.
    Example output:
    ===         subtitle       ===
    """
    banner_width = max(len(subtitle) + 8, min_width)
    padding = banner_width - (len(subtitle) + 8) + 2
    left_pad = padding // 2
    right_pad = padding - left_pad
    return f"==={' ' * left_pad}{subtitle}{' ' * right_pad}==="

def marker_line(length: int = 0, char: str = "-") -> str:
    """Returns a line of repeated characters as a marker.
    If length is undefined, uses the console width.
    If console width is unavailable defaults to 80."""
    width = 0
    try:
        # Try to get terminal size
        width = shutil.get_terminal_size().columns
    except Exception:
        pass  # Fallback to provided length if unable to get terminal size
    if not width and not length:
        length = 80
    elif width and not length:
        length = width
    return char * length

