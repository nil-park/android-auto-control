import logging
import time

import cv2

from .capture import ScreenCapture, locate_server, server_version
from .settings import AndroidAutoControlSettings

_WINDOW_TITLE = "android-auto-control"
_FRAME_LOG_INTERVAL_SECONDS = 60.0

logger = logging.getLogger(__name__)


def run(settings: AndroidAutoControlSettings) -> int:
    """폰 화면을 OpenCV 창에 띄운다. `q`를 누르면 닫는다."""
    jar = locate_server(settings.scrcpy_server)
    version = server_version(jar)
    logger.info(f"Using scrcpy-server {version} at {jar}")

    # KEEPRATIO가 없으면 창이 화면에 잘려 모양이 틀어질 때 이미지가 늘어난다.
    cv2.namedWindow(_WINDOW_TITLE, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    sized = False
    last_size_log = 0.0
    with ScreenCapture(jar, version, settings.max_size) as capture:
        for frame in capture.frames():
            height, width = frame.shape[0], frame.shape[1]
            if not sized:
                cv2.resizeWindow(
                    _WINDOW_TITLE, round(width * settings.display_scale), round(height * settings.display_scale)
                )
                sized = True
            now = time.monotonic()
            if now - last_size_log >= _FRAME_LOG_INTERVAL_SECONDS:
                logger.info(f"Output frame size: {width}x{height}")
                last_size_log = now
            cv2.imshow(_WINDOW_TITLE, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    cv2.destroyAllWindows()
    return 0
