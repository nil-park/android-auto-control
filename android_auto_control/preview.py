import logging
import time
from datetime import UTC, datetime
from pathlib import Path

import cv2

from .capture import BgrFrame, ScreenCapture, locate_server, server_version
from .settings import AndroidAutoControlSettings

_WINDOW_TITLE = "android-auto-control"
_FRAME_LOG_INTERVAL_SECONDS = 60.0
_SCREENSHOT_DIR = Path(".out")

logger = logging.getLogger(__name__)


def _save_screenshot(frame: BgrFrame) -> None:
    _SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).astimezone()
    path = _SCREENSHOT_DIR / f"screenshot-{stamp:%Y%m%d-%H%M%S-%f}.png"
    cv2.imwrite(str(path), frame)
    logger.info(f"Saved screenshot to {path}")


def run(settings: AndroidAutoControlSettings) -> int:
    """폰 화면을 OpenCV 창에 띄운다. `q`를 누르면 종료하고, `c`를 누르면 `.out`에 스크린샷을 저장한다."""
    jar = locate_server(settings.scrcpy_server)
    version = server_version(jar)
    logger.info(f"Using scrcpy-server {version} at {jar}")

    # 창이 이미지를 늘리지 않도록 표시할 프레임을 직접 배율만큼 줄이고 AUTOSIZE 창에 그린다.
    scale = settings.display_scale
    interpolation = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_LINEAR
    last_size_log = 0.0
    with ScreenCapture(jar, version, settings.max_size) as capture:
        for frame in capture.frames():
            height, width = frame.shape[0], frame.shape[1]
            now = time.monotonic()
            if now - last_size_log >= _FRAME_LOG_INTERVAL_SECONDS:
                logger.info(f"Output frame size: {width}x{height}")
                last_size_log = now
            shown = frame if scale == 1.0 else cv2.resize(frame, None, fx=scale, fy=scale, interpolation=interpolation)
            cv2.imshow(_WINDOW_TITLE, shown)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("c"):
                _save_screenshot(frame)
    cv2.destroyAllWindows()
    return 0
