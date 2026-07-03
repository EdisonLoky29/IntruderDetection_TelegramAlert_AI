import time
from datetime import datetime

import cv2

import config
from alarm import Alarm
from alerter import TelegramAlerter
from detector import PersonDetector
from zone import draw_roi, get_center_rectangle_roi, point_in_roi


def log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def person_in_roi(box, roi_polygon) -> bool:
    x1, y1, x2, y2, _ = box
    center_point = ((x1 + x2) // 2, (y1 + y2) // 2)
    return point_in_roi(center_point, roi_polygon)


def main() -> None:
    log("Starting Intruder Detection & Alert System...")

    detector = PersonDetector()
    alarm = Alarm()

    try:
        alerter = TelegramAlerter()
        telegram_enabled = True
    except ValueError as exc:
        log(f"Telegram alerts disabled: {exc}")
        telegram_enabled = False

    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    if not cap.isOpened():
        log(f"Could not open camera index {config.CAMERA_INDEX}.")
        return

    last_alert_time = 0.0
    log("System ready. Press 'q' to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                log("Failed to read frame from camera.")
                break

            frame_height, frame_width = frame.shape[:2]
            roi_polygon = get_center_rectangle_roi(frame_width, frame_height)

            detections = detector.detect_people(frame)
            intrusion = False

            for box in detections:
                x1, y1, x2, y2, conf = box
                inside = person_in_roi(box, roi_polygon)
                if inside:
                    intrusion = True
                color = (0, 0, 255) if inside else (255, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(
                    frame, f"person {conf:.2f}", (x1, max(y1 - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,
                )

            frame = draw_roi(frame, roi_polygon, intrusion)

            status_text = "INTRUSION DETECTED" if intrusion else "Monitoring..."
            status_color = (0, 0, 255) if intrusion else (0, 255, 0)
            cv2.putText(
                frame, status_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2,
            )

            if intrusion:
                now = time.time()
                if now - last_alert_time >= config.ALERT_COOLDOWN_SECONDS:
                    log("Intrusion detected in restricted zone!")
                    alarm.play()
                    if telegram_enabled:
                        if alerter.send_intrusion_alert(frame):
                            log("Telegram alert sent successfully.")
                        else:
                            log("Telegram alert failed to send.")
                    last_alert_time = now

            cv2.imshow("Intruder Detection & Alert System", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                log("Quit signal received. Shutting down.")
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
