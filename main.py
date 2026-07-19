# main.py
import sys
import os
import cv2
import sqlite3
import time

# 1. Database functions
def initialize_db():
    """Creates a local SQLite database and table if it doesn't exist yet."""
    conn = sqlite3.connect("exam_logs.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            violation_type TEXT,
            integrity_score REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_violation(violation_type, integrity_score):
    """Logs a timestamped cheating incident into the local database."""
    conn = sqlite3.connect("exam_logs.db")
    cursor = conn.cursor()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO violations (timestamp, violation_type, integrity_score)
        VALUES (?, ?, ?)
    ''', (timestamp, violation_type, integrity_score))
    conn.commit()
    conn.close()
    print(f"[DATABASE LOG] Recorded entry: {violation_type} at {timestamp}")

# Initialize the database immediately on launch
initialize_db()

# 2. Setup paths for core components
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from core.object_detector import ExamObjectDetector
from core.pose_estimator import ExamPoseEstimator   
from core.integrity_engine import IntegrityEngine
from utils.visualizer import draw_overlays
from utils.alert_system import dispatch_email_alert  

def run_proctor_pipeline():
    cap = cv2.VideoCapture(0)
    detector = ExamObjectDetector()
    pose_tracker = ExamPoseEstimator()               
    engine = IntegrityEngine()

    # Cooldown trackers to prevent sending 1000 emails per second
    last_email_time = 0
    EMAIL_COOLDOWN = 10  # Seconds to wait before allowed to send another email

    print("[SYSTEM INFO] Initializing computer vision proctoring engine...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: 
            print("[ERROR] Camera feed failed.")
            break

        # Run core detection models
        p_count, violations = detector.analyze_frame(frame)
        head_turned = pose_tracker.evaluate_head_gaze(frame) 
        
        frame_compromised = (p_count != 1) or (len(violations) > 0) or head_turned
        alarm_triggered, score = engine.update_and_check(frame_compromised)

        # --- INSTANT TESTING TRIGGERS (Bypassing the engine buffer restriction) ---
        current_time = time.time()
        if frame_compromised and (current_time - last_email_time > EMAIL_COOLDOWN):
            if head_turned:
                reason = "Looking Sideways / Copying"
            elif p_count != 1:
                reason = "Multiple People/No Candidate"
            else:
                reason = "Contraband Detected"

            print(f"\n[ALERT TRIGGERED] Anomaly caught: {reason}")
            
            # 1. Log to DB
            log_violation(reason, score)
            
            # 2. Fire email alert immediately
            print("[ALERT TRIGGERED] Passing frame to email subsystem...")
            dispatch_email_alert(reason, frame)
            
            last_email_time = current_time

        # Render live graphic displays
        display_frame = draw_overlays(frame, p_count, violations, score, alarm_triggered)
        
        if head_turned:
            cv2.putText(display_frame, "WARNING: LOOKING SIDEWAYS", (20, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow("Proctor AI Core Console", display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[SYSTEM INFO] Terminating engine runtime processes...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_proctor_pipeline()