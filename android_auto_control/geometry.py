from dataclasses import dataclass


@dataclass(frozen=True)
class Size:
    width: int
    height: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError(f"size must be positive, got {self.width}x{self.height}")


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class FrameToScreen:
    """캡처 프레임 좌표를 폰 화면 좌표로 옮긴다. scrcpy가 화면을 축소해 보내면 둘의 크기가 다르다."""

    frame: Size
    screen: Size

    def __call__(self, point: Point) -> Point:
        return Point(
            point.x * self.screen.width // self.frame.width,
            point.y * self.screen.height // self.frame.height,
        )
