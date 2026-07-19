# config.py

# Model paths - Ultralytics will auto-download these files on the first run
MODEL_DETECTION_PATH = "yolov8n.pt"  
MODEL_POSE_PATH = "yolov8n-pose.pt"

# Thresholds for object detection
CONFIDENCE_THRESHOLD = 0.50

# History buffer configuration for the integrity scoring engine
TIME_WINDOW_FRAMES = 90
VIOLATION_TRIGGER_PERCENT = 0.40

# =====================================================================
# Email Notification Settings
# =====================================================================
# IMPORTANT: For Gmail, do not use your login password. 
# Generate a 16-character App Password from your Google Account settings.
SENDER_EMAIL = "cvproject1430@gmail.com"
SENDER_PASSWORD = "ukuwkvwqjhilxlxt"  
RECEIVER_EMAIL = "theharshithofficial@gmail.com"       # The email that receives the alert
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587