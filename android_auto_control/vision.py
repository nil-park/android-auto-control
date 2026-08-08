import cv2

from .capture import Frame
from .geometry import Point


def find_template(frame: Frame, template: Frame, threshold: float = 0.9) -> Point | None:
    """템플릿이 가장 잘 맞는 자리의 중심을 프레임 좌표로 돌려준다. 점수가 임계값에 못 미치면 None."""
    frame_height, frame_width = frame.shape[:2]
    template_height, template_width = template.shape[:2]
    if template_height > frame_height or template_width > frame_width:
        raise ValueError(
            f"template {template_width}x{template_height} does not fit in frame {frame_width}x{frame_height}"
        )

    scores = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    _, best_score, _, best_corner = cv2.minMaxLoc(scores)
    if best_score < threshold:
        return None
    return Point(best_corner[0] + template_width // 2, best_corner[1] + template_height // 2)
