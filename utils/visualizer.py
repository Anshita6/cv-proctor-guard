# utils/visualizer.py
import cv2

def draw_overlays(frame, p_count, violations, integrity_score, alarm_triggered):
    output_frame = frame.copy()
    h, w, _ = frame.shape
    
    # Set display color profile based on threat level
    color = (0, 0, 255) if alarm_triggered else (0, 255, 0)
    status_text = "ALERT: FLAGRANT CHEATING DETECTED" if alarm_triggered else "STATUS: SECURE"
    
    # 1. Draw Bounding Boxes for Phones/Books
    for violation in violations:
        bbox = [int(coord) for coord in violation["bbox"]]
        cv2.rectangle(output_frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255), 2)
        cv2.putText(output_frame, violation["item"].upper(), (bbox[0], bbox[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # 2. Add Status Header Bar overlay
    cv2.rectangle(output_frame, (0, 0), (w, 50), (30, 30, 30), -1)
    cv2.putText(output_frame, f"{status_text} | Score: {integrity_score}%", (20, 32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    # 3. Add Candidate presence footer
    cv2.putText(output_frame, f"Candidates in View: {p_count}", (20, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
    return output_frame