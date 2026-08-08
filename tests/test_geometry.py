import pytest

from android_auto_control.geometry import FrameToScreen, Point, Size


@pytest.mark.parametrize(("width", "height"), [(0, 100), (100, 0), (-1, 100)])
def test_size_rejects_non_positive(width: int, height: int) -> None:
    with pytest.raises(ValueError):
        _ = Size(width, height)


def test_frame_to_screen_scales_up() -> None:
    to_screen = FrameToScreen(frame=Size(540, 1200), screen=Size(1080, 2400))
    assert to_screen(Point(100, 200)) == Point(200, 400)


def test_frame_to_screen_keeps_coordinates_when_sizes_match() -> None:
    screen = Size(1080, 2400)
    to_screen = FrameToScreen(frame=screen, screen=screen)
    assert to_screen(Point(37, 41)) == Point(37, 41)


def test_frame_to_screen_keeps_the_last_pixel_inside_the_screen() -> None:
    to_screen = FrameToScreen(frame=Size(540, 1200), screen=Size(1080, 2400))
    assert to_screen(Point(539, 1199)) == Point(1078, 2398)
