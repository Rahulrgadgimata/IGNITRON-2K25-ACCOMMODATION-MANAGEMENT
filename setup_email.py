"""
Email Configuration Setup Script
Run this script to configure your Gmail credentials for automated emails.
"""

import os
import getpass

print("=" * 60)
print("IGNITRON 2K25 - Email Configuration Setup")
print("=" * 60)
print()

print("To use Gmail, you need to create an App Password:")
print("1. Go to your Google Account settings")
print("2. Enable 2-Step Verification")
print("3. Go to Security > App passwords")
print("4. Generate a new app password for 'Mail'")
print()

gmail = input("Enter your Gmail address: ").strip()
password = getpass.getpass("Enter your Gmail App Password: ").strip()

# Create .env file or update config
env_content = f"""# Email Configuration
MAIL_USERNAME={gmail}
MAIL_PASSWORD={password}
"""

# Write to .env file
with open('.env', 'w') as f:
    f.write(env_content)

print()
print("✓ Email configuration saved to .env file")
print("✓ You can also set these as environment variables:")
print(f"  export MAIL_USERNAME={gmail}")
print(f"  export MAIL_PASSWORD=***")
print()
print("Note: Make sure to add .env to .gitignore to keep your credentials secure!")


