"""
Alternative Email Service - Works with different authentication methods
"""
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_booking_approval_email(user_email, user_name, room_no, room_description=None):
    """Send email notification when booking is approved - Enhanced version"""
    try:
        # Get email credentials from config
        sender_email = current_app.config.get('MAIL_USERNAME', '')
        sender_password = current_app.config.get('MAIL_PASSWORD', '')
        
        if not sender_email or not sender_password:
            print("⚠️ Email credentials not configured. Skipping email send.")
            return False
        
        print(f"📧 Attempting to send email to {user_email}...")
        
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = '🎉 Room Booking Approved - IGNITRON 2K25'
        message['From'] = sender_email
        message['To'] = user_email
        
        # Create HTML email content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f4f4f4;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #1a0d2e 0%, #2d1b4e 50%, #1a0d2e 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    letter-spacing: 2px;
                }}
                .content {{
                    padding: 30px;
                }}
                .room-details {{
                    background-color: #f8f9fa;
                    border-left: 4px solid #8b5cf6;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 5px;
                }}
                .room-details h3 {{
                    color: #8b5cf6;
                    margin-top: 0;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background: linear-gradient(135deg, #8b5cf6, #a78bfa);
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    color: #666;
                    font-size: 12px;
                    border-top: 1px solid #eee;
                }}
                .highlight {{
                    color: #8b5cf6;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Booking Approved!</h1>
                    <p>IGNITRON 2K25 Accommodation</p>
                </div>
                <div class="content">
                    <p>Dear <strong>{user_name}</strong>,</p>
                    
                    <p>We are pleased to inform you that your accommodation booking request has been <span class="highlight">APPROVED</span>!</p>
                    
                    <div class="room-details">
                        <h3>📋 Room Allocation Details</h3>
                        <p><strong>Room Number:</strong> <span class="highlight">{room_no}</span></p>
                        {f'<p><strong>Description:</strong> {room_description}</p>' if room_description else ''}
                        <p><strong>Status:</strong> <span class="highlight">Approved</span></p>
                    </div>
                    
                    <p>Your room has been successfully allotted for the IGNITRON 2K25 tech fest. Please note the following:</p>
                    
                    <ul>
                        <li>You can check-in to your room anytime after approval</li>
                        <li>Please bring a valid ID proof during check-in</li>
                        <li>Follow all accommodation guidelines and rules</li>
                        <li>Check-out before the event ends</li>
                    </ul>
                    
                    <p>For any queries or assistance, please contact the accommodation team.</p>
                    
                    <div style="text-align: center;">
                        <a href="http://127.0.0.1:5000/user/dashboard" class="button">View My Booking</a>
                    </div>
                    
                    <p>Best regards,<br>
                    <strong>IGNITRON 2K25 Accommodation Team</strong><br>
                    GM University, Davanagere</p>
                </div>
                <div class="footer">
                    <p>This is an automated email. Please do not reply to this message.</p>
                    <p>&copy; 2025 IGNITRON Tech Fest. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        Booking Approved - IGNITRON 2K25
        
        Dear {user_name},
        
        We are pleased to inform you that your accommodation booking request has been APPROVED!
        
        Room Allocation Details:
        - Room Number: {room_no}
        {f'- Description: {room_description}' if room_description else ''}
        - Status: Approved
        
        Your room has been successfully allotted for the IGNITRON 2K25 tech fest.
        
        Best regards,
        IGNITRON 2K25 Accommodation Team
        GM University, Davanagere
        """
        
        # Create MIMEText objects
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        
        # Attach parts
        message.attach(part1)
        message.attach(part2)
        
        # Try multiple SMTP methods
        print(f"🔗 Connecting to Gmail SMTP server...")
        
        try:
            # Method 1: Standard SMTP with TLS
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.set_debuglevel(0)  # Set to 1 for verbose output
                print(f"🔐 Starting TLS connection...")
                server.starttls()
                print(f"🔑 Authenticating...")
                server.login(sender_email, sender_password)
                print(f"✉️ Sending email message...")
                server.send_message(message)
            
            print(f"✅ Booking approval email sent successfully to {user_email}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            error_code = e.smtp_code if hasattr(e, 'smtp_code') else 'Unknown'
            error_msg = str(e)
            print(f"❌ Gmail Authentication Failed!")
            print(f"   Error Code: {error_code}")
            print(f"   Error: {error_msg}")
            print(f"\n🔧 SOLUTIONS:")
            print(f"   1. Enable 2-Step Verification first:")
            print(f"      👉 https://myaccount.google.com/security")
            print(f"   2. Then create App Password:")
            print(f"      👉 https://myaccount.google.com/apppasswords")
            print(f"   3. OR try enabling 'Less secure app access' (if available)")
            print(f"   4. Update config.py with App Password")
            return False
            
        except Exception as e:
            error_type = type(e).__name__
            print(f"❌ Error sending email to {user_email}")
            print(f"   Error Type: {error_type}")
            print(f"   Error Message: {str(e)}")
            return False
        
    except Exception as e:
        print(f"❌ Unexpected error in email service: {str(e)}")
        return False

