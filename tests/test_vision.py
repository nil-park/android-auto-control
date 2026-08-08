import numpy as np
import pytest

from android_auto_control.capture import Frame
from android_auto_control.geometry import Point
from android_auto_control.vision import find_template


def _noise(width: int, height: int, seed: int) -> Frame:
    return np.random.default_rng(seed).integers(0, 256, size=(height, width, 3), dtype=np.uint8)


def test_find_template_returns_the_center_of_the_match() -> None:
    frame = _noise(200, 100, seed=1)
    template = frame[30:40, 50:60].copy()

    assert find_template(frame, template) == Point(55, 35)


def test_find_template_returns_none_when_the_score_is_below_the_threshold() -> None:
    frame = _noise(200, 100, seed=1)
    template = _noise(10, 10, seed=2)

    assert find_template(frame, template) is None


def test_find_template_rejects_a_template_larger_than_the_frame() -> None:
    with pytest.raises(ValueError):
        _ = find_template(_noise(20, 20, seed=1), _noise(30, 10, seed=2))
