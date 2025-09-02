# app/email_utils.py
# ==================libraries==============================
# smtplib → Python’s library to send emails using SMTP (Simple Mail Transfer Protocol).
# MIMEText → Used to create a simple text email (body + subject + sender/receiver).
# logging → For logging info or errors while sending emails.
# ===============================================

'''
This is a simple email utility function to send text emails via Gmail.
It uses SMTP over SSL to send emails securely.
It logs success or failure for debugging and monitoring.
Always use Gmail App Passwords instead of your real Gmail password.
'''
import smtplib
from email.mime.text import MIMEText
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(subject: str, body: str, to_email: str,
               sender_email: str = "microverse.platform@gmail.com",
               sender_password: str = "nluc vsfo vfsp japj"):
    """
    Send a simple text email using Gmail SMTP over SSL.
    IMPORTANT:
      - Replace sender_email and sender_password with valid credentials.
      - For Gmail, create an App Password and use it here (don't use your Gmail login directly).
    """
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email

        # SMTP over SSL
        # SMTP_SSL("smtp.gmail.com", 465) → Connects securely to Gmail’s SMTP server.
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        logger.info(f"Email sent successfully to {to_email}!")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise e


# # Example usage (can be removed in production)
# if __name__ == "__main__":
#     send_email(
#         subject="Test Email from FastAPI Utils",
#         body="Hello! This is a test email from your email_utils.py",
#         to_email="microverse.platform@gmail.com"
#     )
