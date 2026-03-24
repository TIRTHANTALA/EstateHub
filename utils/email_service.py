"""
Email Service for EstateHub - OTP and notifications
"""
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import config

def generate_otp(length: int = 6) -> str:
    """Generate a random numeric OTP"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(to_email: str, otp: str) -> tuple[bool, str]:
    """Send OTP email for password reset"""
    if not config.EMAIL_ADDRESS or not config.EMAIL_PASSWORD:
        return False, "Email service not configured. Please contact admin."
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "EstateHub - Password Reset OTP"
        msg['From'] = config.EMAIL_ADDRESS
        msg['To'] = to_email
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }}
                .container {{ max-width: 500px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; margin-bottom: 20px; }}
                .logo {{ font-size: 24px; font-weight: bold; color: #6366f1; }}
                .otp-box {{ background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; font-size: 32px; font-weight: bold; text-align: center; padding: 20px; border-radius: 10px; letter-spacing: 8px; margin: 20px 0; }}
                .message {{ color: #64748b; line-height: 1.6; }}
                .footer {{ text-align: center; margin-top: 20px; color: #94a3b8; font-size: 12px; }}
                .warning {{ background: #fef3c7; color: #92400e; padding: 10px; border-radius: 5px; margin-top: 15px; font-size: 13px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">🏠 EstateHub</div>
                </div>
                <p class="message">Hello,</p>
                <p class="message">You have requested to reset your password. Use the OTP below to proceed:</p>
                <div class="otp-box">{otp}</div>
                <p class="message">This OTP is valid for <strong>{config.OTP_EXPIRY_MINUTES} minutes</strong>.</p>
                <div class="warning">
                    ⚠️ If you didn't request this, please ignore this email. Your password will remain unchanged.
                </div>
                <div class="footer">
                    <p>© 2026 EstateHub. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        EstateHub - Password Reset
        
        Your OTP for password reset is: {otp}
        
        This OTP is valid for {config.OTP_EXPIRY_MINUTES} minutes.
        
        If you didn't request this, please ignore this email.
        """
        
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        with smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT) as server:
            server.starttls()
            server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
            server.send_message(msg)
        
        return True, "OTP sent successfully"
    
    except smtplib.SMTPAuthenticationError:
        return False, "Email authentication failed. Check email credentials."
    except smtplib.SMTPException as e:
        return False, f"Failed to send email: {str(e)}"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

def get_otp_expiry() -> datetime:
    """Get OTP expiry timestamp"""
    return datetime.utcnow() + timedelta(minutes=config.OTP_EXPIRY_MINUTES)

def is_otp_expired(expiry_time: datetime) -> bool:
    """Check if OTP has expired"""
    return datetime.utcnow() > expiry_time
