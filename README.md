# cv-proctor-guide

An AI-powered exam proctoring system that monitors webcam video in real time to detect signs of cheating (unusual poses, unauthorized objects, and behavioral anomalies), and can send automated email alerts.

## Features

- **Pose estimation** — tracks candidate posture/movement using YOLOv8-Pose (`yolov8n-pose.pt`)
- **Object detection** — flags unauthorized objects (e.g. phones, notes) using YOLOv8 (`yolov8n.pt`)
- **Integrity scoring engine** — maintains a rolling window of anomaly frames and computes a live integrity score
- **Email alerts** — sends verification/notification emails via Gmail SMTP (`check_link.py`)
- **Session logging** — stores exam session logs in a local SQLite database (`exam_logs.db`)

## Project Structure

```
exam-proctor-ai/
├── core/
│   ├── __init__.py
│   ├── integrity_engine.py   # Anomaly buffer + integrity score calculation
│   ├── object_detector.py    # YOLO-based object detection
│   └── pose_estimator.py     # YOLO-based pose estimation
├── utils/                    # Helper utilities
├── check_link.py             # SMTP connectivity / email verification check
├── config.py                 # Configuration (SMTP, thresholds, etc.)
├── database.py                # Database read/write helpers
├── exam_logs.db               # SQLite database of exam session logs
├── main.py                    # Application entry point
├── yolov8n-pose.pt            # YOLOv8 pose estimation model weights
└── yolov8n.pt                 # YOLOv8 object detection model weights
```

## Requirements

- Python 3.10+ (tested on 3.14)
- pip

### Python packages

This project doesn't ship a `requirements.txt` yet — install manually:

```bash
python -m pip install opencv-python ultralytics numpy
```

> If you add more imports later, consider generating a proper `requirements.txt` with:
> ```bash
> python -m pip freeze > requirements.txt
> ```

## Setup

1. **Clone or download this project.**

2. **Install dependencies** (see above).

3. **Configure email settings** in `config.py`:
   ```python
   SMTP_SERVER = "smtp.gmail.com"
   SMTP_PORT = 587
   SENDER_EMAIL = "your-email@gmail.com"
   SENDER_PASSWORD = "your-app-password"   # Use a Gmail App Password, not your normal password
   ```
   > Gmail requires an **App Password** (not your regular login password) when 2FA is enabled. Generate one at: Google Account → Security → App Passwords.

4. **Verify email connectivity** (optional but recommended):
   ```bash
   python check_link.py
   ```

## Running the Project

```bash
python main.py
```

This launches the main proctoring application (webcam feed, pose/object detection, and integrity scoring).

To stop it, click into the terminal (or the camera window, if one opens) and press `Ctrl + C` (or `q` if the video window supports it).

## Configuration Notes

- `TIME_WINDOW_FRAMES` in `config.py` controls how many recent frames are used to compute the rolling integrity score.
- The integrity score starts at `100.0` during a warm-up phase (before enough frames have been collected) and decreases as anomalies accumulate.

## Troubleshooting

| Issue | Fix |
|---|---|
| `python` not recognized | Reinstall Python from python.org and check "Add python.exe to PATH" during install |
| `pip` not recognized | Use `python -m pip ...` instead of `pip ...` |
| `ModuleNotFoundError` | Install the missing package with `python -m pip install <package-name>` |
| SMTP login fails | Confirm you're using a Gmail **App Password**, and that `SMTP_SERVER`/`SMTP_PORT` are correct |
