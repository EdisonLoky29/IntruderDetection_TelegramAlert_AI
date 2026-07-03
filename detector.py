from ultralytics import YOLO

import config

PERSON_CLASS_ID = 0 


class PersonDetector:
    def __init__(self, model_path: str = None, confidence: float = None):
        self.model = YOLO(model_path or config.MODEL_PATH)
        self.confidence = confidence or config.CONFIDENCE_THRESHOLD

    def detect_people(self, frame):
        results = self.model.predict(
            frame,
            device="cpu",
            classes=[PERSON_CLASS_ID],
            conf=self.confidence,
            verbose=False,
        )

        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                detections.append((int(x1), int(y1), int(x2), int(y2), conf))
        return detections
