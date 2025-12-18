import pytest
from pyutils.markers import title, subtitle, marker_line


def test_title_default():
    # Should use the caller's filename if no title is given
    result = title()
    assert isinstance(result, str)
    assert '===' in result
    assert result.count('\n') == 3


def test_title_custom():
    result = title("MyTitle", min_width=30)
    assert "MyTitle" in result
    assert result.startswith("\n")
    assert result.count("=") > 0


def test_subtitle():
    result = subtitle("Sub", min_width=20)
    assert "Sub" in result
    assert result.startswith("===")
    assert result.endswith("===")


def test_marker_line_default(monkeypatch):
    # Simulate terminal width
    monkeypatch.setattr("shutil.get_terminal_size", lambda: type('T', (), {'columns': 50})())
    line = marker_line()
    assert isinstance(line, str)
    assert len(line) == 50
    assert set(line) == {'-'}


def test_marker_line_length():
    line = marker_line(length=10)
    assert len(line) == 10
    assert set(line) == {'-'}


def test_marker_line_char():
    line = marker_line(length=8, char="*")
    assert line == "********"


def test_marker_line_no_terminal(monkeypatch):
    # Simulate failure to get terminal size
    monkeypatch.setattr("shutil.get_terminal_size", lambda: (_ for _ in ()).throw(OSError()))
    line = marker_line()
    assert isinstance(line, str)
    assert len(line) == 80
    assert set(line) == {'-'}

