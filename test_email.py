"""
Test script to verify email configuration
Run this to test if your email credentials work
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Import from config
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from config import Config
    config = Config()
    SENDER_EMAIL = config.MAIL_USERNAME
    SENDER_PASSWORD = config.MAIL_PASSWORD
except:
    # Fallback
    SENDER_EMAIL = "chutiyaabhiram@gmail.com"
    SENDER_PASSWORD = "Rahul@1704"

RECIPIENT_EMAIL = "rahulrgadgimata@gmail.com"  # Send test to yourself

def test_email():
    try:
        print("Testing email configuration...")
        print(f"Sender: {SENDER_EMAIL}")
        
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Test Email - IGNITRON 2K25'
        message['From'] = SENDER_EMAIL
        message['To'] = RECIPIENT_EMAIL
        
        # Create email content
        html_content = """
        <html>
        <body>
            <h2>Email Test Successful!</h2>
            <p>Your email configuration is working correctly.</p>
            <p>IGNITRON 2K25 Accommodation System</p>
        </body>
        </html>
        """
        
        text_content = "Email Test Successful! Your email configuration is working correctly."
        
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        
        message.attach(part1)
        message.attach(part2)
        
        # Connect to Gmail SMTP server
        print("Connecting to Gmail SMTP server...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            print("Logging in...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("Sending test email...")
            server.send_message(message)
        
        print("✅ SUCCESS! Test email sent successfully!")
        print(f"Check your inbox at: {RECIPIENT_EMAIL}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("❌ AUTHENTICATION ERROR!")
        print("This usually means:")
        print("1. Your password is incorrect, OR")
        print("2. You need to use a Gmail App Password instead of your regular password")
        print()
        print("To create an App Password:")
        print("1. Go to https://myaccount.google.com/security")
        print("2. Enable 2-Step Verification")
        print("3. Go to App passwords")
        print("4. Generate a new app password for 'Mail'")
        print("5. Use that 16-character password instead")
        print()
        print(f"Error details: {e}")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_email()

