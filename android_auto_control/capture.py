from typing import Protocol

import numpy as np
from numpy.typing import NDArray

from .geometry import Size

Frame = NDArray[np.uint8]
"""BGR 순서의 (height, width, 3) 배열. OpenCV가 쓰는 그대로다."""


class FrameSource(Protocol):
    """폰 화면을 프레임 단위로 내보낸다."""

    @property
    def frame_size(self) -> Size: ...

    def read(self) -> Frame | None:
        """다음 프레임을 돌려준다. 스트림이 끝났으면 None."""
        ...
