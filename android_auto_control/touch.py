from types import TracebackType
from typing import Protocol, Self

import serial

from .geometry import Point, Size

_ENCODING = "ascii"
_ACK = "OK"

DEFAULT_TAP_DURATION_MS = 80


class TouchDeviceError(RuntimeError):
    pass


class TouchDevice(Protocol):
    """폰에 터치를 넣는다. 좌표는 폰 화면 픽셀이다."""

    @property
    def screen(self) -> Size: ...

    def tap(self, point: Point, duration_ms: int = DEFAULT_TAP_DURATION_MS) -> None: ...


def _command(*parts: object) -> bytes:
    return (" ".join(str(part) for part in parts) + "\n").encode(_ENCODING)


def encode_screen_size(screen: Size) -> bytes:
    return _command("S", screen.width, screen.height)


def encode_tap(point: Point, duration_ms: int) -> bytes:
    return _command("T", point.x, point.y, duration_ms)


def encode_press(point: Point) -> bytes:
    return _command("D", point.x, point.y)


def encode_move(point: Point) -> bytes:
    return _command("M", point.x, point.y)


def encode_release() -> bytes:
    return _command("U")


class SerialTouchDevice:
    """USB 시리얼로 붙은 ESP32. 명령마다 응답을 확인하므로 한 번에 한 명령만 보낸다."""

    def __init__(self, port: str, screen: Size, *, baudrate: int = 115200, timeout_s: float = 1.0) -> None:
        self._screen = screen
        self._port = serial.Serial(port, baudrate=baudrate, timeout=timeout_s)
        try:
            self._send(encode_screen_size(screen))
        except BaseException:
            self.close()
            raise

    @property
    def screen(self) -> Size:
        return self._screen

    def tap(self, point: Point, duration_ms: int = DEFAULT_TAP_DURATION_MS) -> None:
        self._send(encode_tap(point, duration_ms))

    def press(self, point: Point) -> None:
        self._send(encode_press(point))

    def move(self, point: Point) -> None:
        self._send(encode_move(point))

    def release(self) -> None:
        self._send(encode_release())

    def close(self) -> None:
        self._port.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def _send(self, command: bytes) -> None:
        _ = self._port.write(command)
        # 잡음이 섞인 라인도 TouchDeviceError로 나가야 하므로 디코딩에서 터뜨리지 않는다.
        answer = self._port.readline().decode(_ENCODING, errors="replace").strip()
        if answer != _ACK:
            raise TouchDeviceError(f"{command.decode(_ENCODING).strip()!r} was answered with {answer!r}")
