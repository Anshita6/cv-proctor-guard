# core/pose_estimator.py
from ultralytics import YOLO
import numpy as np
import config

class ExamPoseEstimator:
    def __init__(self):
        # Load the pose-estimation specific weight architecture
        self.pose_model = YOLO(config.MODEL_POSE_PATH)
        # Asymmetry threshold: 0.0 is dead-center, >0.6 means looking far left/right
        self.turn_threshold = 0.55 

    def evaluate_head_gaze(self, frame):
        """
        Extracts facial keypoints to determine if the candidate is looking sideways.
        Returns: True if head turn violation detected, False otherwise.
        """
        results = self.pose_model(frame, verbose=False)[0]
        
        # Ensure at least one person's skeleton is detected
        if results.keypoints is None or len(results.keypoints.xy) == 0:
            return False
            
        # Get keypoint coordinate arrays for the first person detected
        # shape: (num_keypoints, 2) -> xy coordinates
        keypoints = results.keypoints.xy[0].cpu().numpy()
        
        # Validate that the model has high-confidence visibility on nose and ears
        # Check if the coordinates are non-zero placeholders
        if len(keypoints) > 4:
            nose = keypoints[0]
            left_ear = keypoints[3]
            right_ear = keypoints[4]
            
            # If any crucial point is missing (0.0 coordinates), skip calculation
            if np.any(nose == 0) or np.any(left_ear == 0) or np.any(right_ear == 0):
                return False
                
            # Calculate simple horizontal pixel distances (X-axis delta)
            dist_left = abs(nose[0] - left_ear[0])
            dist_right = abs(nose[0] - right_ear[0])
            
            # Prevent Division-by-Zero errors
            if (dist_left + dist_right) == 0:
                return False
                
            # Compute structural asymmetry index
            asymmetry = abs(dist_left - dist_right) / (dist_left + dist_right)
            
            # If the asymmetry ratio crosses the threshold, flag a violation
            if asymmetry > self.turn_threshold:
                return True
                
        return False