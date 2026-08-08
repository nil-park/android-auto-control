import argparse

import pytest

from android_auto_control.__main__ import _parse_size  # pyright: ignore[reportPrivateUsage]
from android_auto_control.geometry import Size


def test_screen_size_is_parsed() -> None:
    assert _parse_size("1080x2400") == Size(1080, 2400)


@pytest.mark.parametrize("text", ["1080", "1080x", "1080*2400", "-1080x2400", "1080 x 2400", ""])
def test_a_malformed_screen_size_is_rejected(text: str) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        _ = _parse_size(text)


def test_a_zero_screen_size_is_rejected() -> None:
    with pytest.raises(ValueError):
        _ = _parse_size("0x2400")
