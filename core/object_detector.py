# core/object_detector.py
from ultralytics import YOLO
import config

class ExamObjectDetector:
    def __init__(self):
        # Native end-to-end NMS-free model loading
        self.model = YOLO(config.MODEL_DETECTION_PATH) 

    def analyze_frame(self, frame):
        results = self.model(frame, verbose=False)[0]
        person_count = 0
        contraband_found = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]
            conf = float(box.conf[0])

            if label == "person":
                person_count += 1
            elif label in ["cell phone", "book"] and conf > config.CONFIDENCE_THRESHOLD:
                contraband_found.append({"item": label, "bbox": box.xyxy[0].tolist()})

        return person_count, contraband_found