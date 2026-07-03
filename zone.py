import numpy as np
import cv2

import config


def get_center_rectangle_roi(frame_width: int, frame_height: int) -> np.ndarray:
    roi_w = int(frame_width * 0.85)
    roi_h = int(frame_height * 0.85)
    x1 = (frame_width - roi_w) // 2
    y1 = (frame_height - roi_h) // 2
    x2 = x1 + roi_w
    y2 = y1 + roi_h
    return np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype=np.int32)


def point_in_roi(point: tuple[int, int], roi_polygon: np.ndarray) -> bool:
    result = cv2.pointPolygonTest(roi_polygon, point, False)
    return result >= 0


def draw_roi(frame, roi_polygon: np.ndarray, intrusion: bool = False):
    color = (0, 0, 255) if intrusion else (0, 255, 0)
    overlay = frame.copy()
    cv2.fillPoly(overlay, [roi_polygon], color)
    cv2.addWeighted(overlay, 0.15, frame, 0.85, 0, frame)
    cv2.polylines(frame, [roi_polygon], isClosed=True, color=color, thickness=2)
    return frame
