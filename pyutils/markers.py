import os
import inspect
import shutil

__all__ = [
    "title",
    "subtitle",
    "marker_line",
]

def _get_console_width() -> int:
    """Get the current console width, or -1 if unavailable."""
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return -1

def _select_width(user_desired_width: int, text_induced_width:int) -> int:
    """Select the appropriate width based on user desire, console width, and text-induced width."""
    console_width = _get_console_width()
    final_width = 0
    if user_desired_width <= 0 and console_width <= 0:
        final_width = text_induced_width
    elif user_desired_width > 0:
        final_width = max(user_desired_width, text_induced_width)
    elif console_width > 0:
        final_width = max(console_width, text_induced_width)
    else:
        raise ValueError(f"Couldn't determine appropriate width. Arguments: user_desired_width={user_desired_width}, console_width={console_width}, text_induced_width={text_induced_width}")
    return final_width


def title(title: str = None, width: int = 0) -> str:
    """Returns a title banner.
    If no title is provided, the caller's filename is used.
    If you do not specify a width, console width is used if available.
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

    text_induced_width = len(title) + 8
    banner_width = _select_width(width, text_induced_width)
    padding = banner_width - (len(title) + 8) + 2
    left_pad = padding // 2
    right_pad = padding - left_pad
    line = "=" * banner_width
    return f"{line}\n==={' ' * left_pad}{title}{' ' * right_pad}===\n{line}"

def subtitle(subtitle, width: int = 0) -> str:
    """Returns a subtitle banner.
    If you do not specify a width, console width is used if available.
    Example output:
    ===         subtitle       ===
    """
    if width:
        banner_width = max(len(subtitle) + 8, width)
    if not width:
        banner_width = max(len(subtitle) + 8, _get_console_width())

    text_induced_width = len(subtitle) + 8
    banner_width = _select_width(width, text_induced_width)
    padding = banner_width - (len(subtitle) + 8) + 2
    left_pad = padding // 2
    right_pad = padding - left_pad
    return f"==={' ' * left_pad}{subtitle}{' ' * right_pad}==="

def marker_line(length: int = 0, char: str = "-") -> str:
    """Returns a line of repeated characters as a marker.
    If length is undefined, uses the console width.
    If console width is unavailable defaults to 80."""
    width = _get_console_width()
    if not width and not length:
        length = 80
    elif width and not length:
        length = width
    return char * length