"""
Gmail App Password Setup Helper
This script helps you set up Gmail App Password for email notifications
"""

print("=" * 70)
print(" GMAIL APP PASSWORD SETUP FOR IGNITRON 2K25")
print("=" * 70)
print()

print("📧 Your email is already configured: chutiyaabhiram@gmail.com")
print()
print("⚠️  IMPORTANT: Gmail requires an 'App Password', not your regular password!")
print()
print("=" * 70)
print(" STEP-BY-STEP INSTRUCTIONS:")
print("=" * 70)
print()

print("STEP 1: Go to Google Account App Passwords")
print("   👉 https://myaccount.google.com/apppasswords")
print()

print("STEP 2: Enable 2-Step Verification (if not already enabled)")
print("   👉 Go to: https://myaccount.google.com/security")
print("   👉 Click '2-Step Verification' and follow instructions")
print()

print("STEP 3: Generate App Password")
print("   1. On App Passwords page, select:")
print("      - App: Mail")
print("      - Device: Other (Custom name)")
print("   2. Enter: 'IGNITRON Accommodation'")
print("   3. Click 'Generate'")
print("   4. Copy the 16-character password")
print("      (Example: abcd efgh ijkl mnop)")
print()

print("STEP 4: Update Configuration")
print("   After getting the App Password, update config.py:")
print("   MAIL_PASSWORD = 'your-16-character-app-password'")
print()

print("=" * 70)
print()

choice = input("Have you created the App Password? (yes/no): ").strip().lower()

if choice in ['yes', 'y']:
    app_password = input("\nEnter your 16-character App Password (without spaces): ").strip()
    
    # Read current config
    try:
        with open('config.py', 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        # Update password in config
        import re
        # Replace the password line
        pattern = r"MAIL_PASSWORD\s*=\s*os\.environ\.get\('MAIL_PASSWORD'\)\s*or\s*'[^']*'"
        replacement = f"MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '{app_password}'"
        
        updated_config = re.sub(pattern, replacement, config_content)
        
        # Write back
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(updated_config)
        
        print("\n✅ Password updated in config.py!")
        print("\n📝 Testing email configuration...")
        
        # Test email
        import test_email
        print("\nRun 'python test_email.py' to verify the setup works!")
        
    except Exception as e:
        print(f"\n❌ Error updating config: {e}")
        print("\nPlease manually update config.py with your App Password:")
        print(f"   MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '{app_password}'")
else:
    print("\n📋 Follow the steps above to create your App Password.")
    print("   Then run this script again or manually update config.py")

print("\n" + "=" * 70)

