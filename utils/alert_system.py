# utils/alert_system.py
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import cv2
import time
import config

def dispatch_email_alert(violation_reason, frame):
    """
    Encodes the visual matrix frame to a standard JPEG buffer format,
    packages it into a multipart MIME payload, and ships it via secure SMTP.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Setup multi-part container payload
    msg = MIMEMultipart()
    msg['From'] = config.SENDER_EMAIL
    msg['To'] = config.RECEIVER_EMAIL
    msg['Subject'] = f"[CRITICAL SECURITY ALERT] Anomaly Detected - {timestamp}"
    
    body = f"""
    Warning: The AI Exam Proctoring Engine has detected an integrity breach.
    
    Incident Parameters:
    -------------------------------------------
    Violation Type : {violation_reason}
    Timestamp      : {timestamp}
    System Status  : Saved to secure local database logs.
    -------------------------------------------
    
    Please review the attached camera evidence snapshot below.
    """
    msg.attach(MIMEText(body, 'plain'))
    
    # 2. Convert raw frame matrix to standard JPEG image bytes
    success, encoded_image = cv2.imencode('.jpg', frame)
    if success:
        image_bytes = encoded_image.tobytes()
        image_attachment = MIMEImage(image_bytes, name=f"evidence_{int(time.time())}.jpg")
        msg.attach(image_attachment)
    else:
        print("[MAIL ERROR] Failed to compress image frame data.")
        return

    # 3. Create SSL Context and send
    context = ssl.create_default_context()
    try:
        print(f"[MAIL SYSTEM] Connecting to server {config.SMTP_SERVER}...")
        server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        server.starttls(context=context)  # Secure the channel
        
        server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
        server.sendmail(config.SENDER_EMAIL, config.RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"📧 [MAIL DISPATCH] Success! Evidence snapshot sent to {config.RECEIVER_EMAIL}")
    except Exception as e:
        print(f"❌ [MAIL SYSTEM CRASH] Transaction failed: {e}")