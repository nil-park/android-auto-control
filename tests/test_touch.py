import pytest

from android_auto_control import touch
from android_auto_control.geometry import Point, Size
from android_auto_control.touch import (
    SerialTouchDevice,
    TouchDeviceError,
    encode_move,
    encode_press,
    encode_release,
    encode_screen_size,
    encode_tap,
)


class _FakeSerialPort:
    def __init__(self, answers: list[bytes]) -> None:
        self.written: list[bytes] = []
        self.closed = False
        self._answers = answers

    def write(self, data: bytes) -> int:
        self.written.append(data)
        return len(data)

    def readline(self) -> bytes:
        return self._answers.pop(0) if self._answers else b""

    def close(self) -> None:
        self.closed = True


def _attach(monkeypatch: pytest.MonkeyPatch, answers: list[bytes]) -> _FakeSerialPort:
    port = _FakeSerialPort(answers)

    def factory(*_args: object, **_kwargs: object) -> _FakeSerialPort:
        return port

    monkeypatch.setattr(touch.serial, "Serial", factory)
    return port


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        (encode_screen_size(Size(1080, 2400)), b"S 1080 2400\n"),
        (encode_tap(Point(10, 20), 80), b"T 10 20 80\n"),
        (encode_press(Point(10, 20)), b"D 10 20\n"),
        (encode_move(Point(30, 40)), b"M 30 40\n"),
        (encode_release(), b"U\n"),
    ],
)
def test_encoders_match_the_serial_protocol(command: bytes, expected: bytes) -> None:
    assert command == expected


def test_connecting_announces_the_screen_size(monkeypatch: pytest.MonkeyPatch) -> None:
    port = _attach(monkeypatch, [b"OK\n"])

    _ = SerialTouchDevice("COM3", Size(1080, 2400))

    assert port.written == [b"S 1080 2400\n"]


def test_tap_sends_the_tap_command(monkeypatch: pytest.MonkeyPatch) -> None:
    port = _attach(monkeypatch, [b"OK\n", b"OK\n"])

    SerialTouchDevice("COM3", Size(1080, 2400)).tap(Point(100, 200), duration_ms=50)

    assert port.written[-1] == b"T 100 200 50\n"


@pytest.mark.parametrize("answer", [b"ERR busy\n", b""])
def test_a_command_that_is_not_acknowledged_raises(monkeypatch: pytest.MonkeyPatch, answer: bytes) -> None:
    _ = _attach(monkeypatch, [answer])

    with pytest.raises(TouchDeviceError):
        _ = SerialTouchDevice("COM3", Size(1080, 2400))


def test_a_failed_handshake_closes_the_port(monkeypatch: pytest.MonkeyPatch) -> None:
    port = _attach(monkeypatch, [b"ERR busy\n"])

    with pytest.raises(TouchDeviceError):
        _ = SerialTouchDevice("COM3", Size(1080, 2400))

    assert port.closed


def test_leaving_the_context_closes_the_port(monkeypatch: pytest.MonkeyPatch) -> None:
    port = _attach(monkeypatch, [b"OK\n"])

    with SerialTouchDevice("COM3", Size(1080, 2400)):
        assert not port.closed

    assert port.closed
