import pytest
from pyutils.markers import title, subtitle, marker_line


def test_title_default(monkeypatch):
    # Should use the caller's filename if no title is given
    monkeypatch.setattr("pyutils.markers._get_console_width", lambda: 40)
    result = title()
    assert isinstance(result, str)
    assert '===' in result
    assert result.count('\n') == 2


def test_title_custom(monkeypatch):
    monkeypatch.setattr("pyutils.markers._get_console_width", lambda: 30)
    result = title("MyTitle")
    assert "MyTitle" in result
    assert result.count("=") > 0


def test_subtitle(monkeypatch):
    monkeypatch.setattr("pyutils.markers._get_console_width", lambda: 20)
    result = subtitle("Sub")
    assert "Sub" in result
    assert result.startswith("===")
    assert result.endswith("===")


def test_marker_line_default(monkeypatch):
    monkeypatch.setattr("pyutils.markers._get_console_width", lambda: 50)
    line = marker_line()
    assert isinstance(line, str)
    assert len(line) == 50
    assert set(line) == {'-'}


def test_marker_line_length(monkeypatch):
    monkeypatch.setattr("pyutils.markers._get_console_width", lambda: 0)
    line = marker_line(length=10)
    assert len(line) == 10
    assert set(line) == {'-'}


def test_marker_line_char(monkeypatch):
    monkeypatch.setattr("pyutils.markers._get_console_width", lambda: 0)
    line = marker_line(length=8, char="*")
    assert line == "********"


def test_marker_line_no_terminal(monkeypatch):
    monkeypatch.setattr("pyutils.markers._get_console_width", lambda: 0)
    line = marker_line()
    assert isinstance(line, str)
    assert len(line) == 80
    assert set(line) == {'-'}
