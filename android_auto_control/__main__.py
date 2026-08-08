import argparse

from .geometry import Point, Size
from .touch import SerialTouchDevice


def _parse_size(text: str) -> Size:
    width, _, height = text.partition("x")
    if not width.isdigit() or not height.isdigit():
        raise argparse.ArgumentTypeError(f"expected WIDTHxHEIGHT, got {text!r}")
    return Size(int(width), int(height))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="android-auto-control",
        description="Send a single tap through the BLE touch device to check that the input path works.",
    )
    parser.add_argument("--port", required=True, help="serial port the ESP32 is attached to, e.g. COM3")
    parser.add_argument("--screen", required=True, type=_parse_size, metavar="WIDTHxHEIGHT", help="phone screen size")
    parser.add_argument("x", type=int, help="tap position in phone screen pixels")
    parser.add_argument("y", type=int, help="tap position in phone screen pixels")
    arguments = parser.parse_args()

    with SerialTouchDevice(arguments.port, arguments.screen) as device:
        device.tap(Point(arguments.x, arguments.y))


if __name__ == "__main__":
    main()
