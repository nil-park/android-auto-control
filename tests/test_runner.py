import numpy as np

from android_auto_control.capture import Frame
from android_auto_control.geometry import Point, Size
from android_auto_control.runner import run_once


class _FakeSource:
    def __init__(self, frames: list[Frame], frame_size: Size) -> None:
        self._frames = frames
        self._frame_size = frame_size

    @property
    def frame_size(self) -> Size:
        return self._frame_size

    def read(self) -> Frame | None:
        return self._frames.pop(0) if self._frames else None


class _FakeDevice:
    def __init__(self, screen: Size) -> None:
        self.taps: list[Point] = []
        self._screen = screen

    @property
    def screen(self) -> Size:
        return self._screen

    def tap(self, point: Point, duration_ms: int = 80) -> None:
        self.taps.append(point)


def _frame_with_template_at(x: int, y: int) -> tuple[Frame, Frame]:
    frame: Frame = np.random.default_rng(7).integers(0, 256, size=(120, 60, 3), dtype=np.uint8)
    return frame, frame[y : y + 10, x : x + 10].copy()


def test_a_match_is_tapped_in_screen_coordinates() -> None:
    frame, template = _frame_with_template_at(20, 40)
    source = _FakeSource([frame], frame_size=Size(60, 120))
    device = _FakeDevice(screen=Size(1080, 2160))

    assert run_once(source, template, device)
    assert device.taps == [Point(450, 810)]


def test_an_exhausted_source_taps_nothing() -> None:
    _, template = _frame_with_template_at(20, 40)
    source = _FakeSource([], frame_size=Size(60, 120))
    device = _FakeDevice(screen=Size(1080, 2160))

    assert not run_once(source, template, device)
    assert device.taps == []


def test_a_frame_without_the_template_taps_nothing() -> None:
    frame, _ = _frame_with_template_at(20, 40)
    other: Frame = np.random.default_rng(8).integers(0, 256, size=(10, 10, 3), dtype=np.uint8)
    source = _FakeSource([frame], frame_size=Size(60, 120))
    device = _FakeDevice(screen=Size(1080, 2160))

    assert not run_once(source, other, device)
    assert device.taps == []
