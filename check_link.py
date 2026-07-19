# check_link.py
import smtplib
import ssl
import config

print("[1/3] Initiating secure SSL context...")
context = ssl.create_default_context()

try:
    print(f"[2/3] Connecting to Google SMTP server for: {config.SENDER_EMAIL}...")
    server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    server.starttls(context=context) 
    
    print("[3/3] Attempting secure login verification...")
    server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
    
    # Send basic verification message payload
    msg = f"Subject: Connection Verified\n\nProctor Engine link is working."
    
    # FIXED LINE HERE (Removed the extra .config)
    server.sendmail(config.SENDER_EMAIL, config.RECEIVER_EMAIL, msg)
    server.quit()
    print("\n✅ SUCCESS! The email interface has successfully verified and linked.")
    
except smtplib.SMTPAuthenticationError as auth_err:
    print("\n❌ AUTHENTICATION ERROR: Google rejected the login credentials.")
    print(f"Error Details: {auth_err}")
except Exception as e:
    print(f"\n❌ ERROR DETECTED: {e}")