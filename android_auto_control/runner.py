from .capture import Frame, FrameSource
from .geometry import FrameToScreen
from .touch import TouchDevice
from .vision import DEFAULT_THRESHOLD, find_template


def run_once(source: FrameSource, template: Frame, device: TouchDevice, threshold: float = DEFAULT_THRESHOLD) -> bool:
    """프레임을 한 장 보고 템플릿이 있으면 그 자리를 누른다. 눌렀으면 True."""
    frame = source.read()
    if frame is None:
        return False

    found = find_template(frame, template, threshold)
    if found is None:
        return False

    to_screen = FrameToScreen(source.frame_size, device.screen)
    device.tap(to_screen(found))
    return True
