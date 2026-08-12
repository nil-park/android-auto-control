import logging

import cv2

from .capture import ScreenCapture, locate_server, server_version
from .settings import AndroidAutoControlSettings

_WINDOW_TITLE = "android-auto-control"

logger = logging.getLogger(__name__)


def run(settings: AndroidAutoControlSettings) -> int:
    """폰 화면을 OpenCV 창에 띄운다. `q`를 누르면 닫는다."""
    jar = locate_server(settings.scrcpy_server)
    version = server_version(jar)
    logger.info(f"Using scrcpy-server {version} at {jar}")

    cv2.namedWindow(_WINDOW_TITLE, cv2.WINDOW_NORMAL)
    with ScreenCapture(jar, version, settings.max_size) as capture:
        for frame in capture.frames():
            cv2.imshow(_WINDOW_TITLE, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    cv2.destroyAllWindows()
    return 0
