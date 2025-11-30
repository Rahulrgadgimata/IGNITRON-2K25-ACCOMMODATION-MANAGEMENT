# How to Enable Gmail App Passwords - Step by Step Guide

## Problem
You're seeing: "The setting you are looking for is not available for your account"

This means you need to **enable 2-Step Verification first** before App Passwords become available.

## Step-by-Step Solution

### STEP 1: Enable 2-Step Verification

1. Go to your Google Account Security page:
   👉 https://myaccount.google.com/security

2. Find the section called **"2-Step Verification"** 
   - It should be in the middle of the page
   - Look for the section with a lock icon

3. Click on **"Get Started"** or **"Turn On"** button

4. Follow the setup wizard:
   - Enter your phone number
   - Choose verification method (SMS or phone call)
   - Enter the verification code sent to your phone
   - Confirm to enable

5. Wait for confirmation that 2-Step Verification is now ON

### STEP 2: Access App Passwords (Now Available!)

1. After enabling 2-Step Verification, go to:
   👉 https://myaccount.google.com/apppasswords

2. **Now you should see the App Passwords page!** (Not the error anymore)

3. On the App Passwords page:
   - **Select app**: Choose "Mail"
   - **Select device**: Choose "Other (Custom name)"
   - **Enter name**: Type "IGNITRON Accommodation"
   - Click **"Generate"**

4. **Copy the 16-character password** immediately!
   - It will look like: `abcd efgh ijkl mnop`
   - Copy it now (you can't see it again later!)
   - Remove spaces when using it

### STEP 3: Update Your Configuration

After you have the App Password, update `config.py`:

1. Open `config.py` in your editor

2. Find line 14 (the MAIL_PASSWORD line)

3. Replace it with:
   ```python
   MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'YOUR-16-CHAR-APP-PASSWORD-HERE'
   ```
   (Paste your App Password without spaces)

4. Save the file

5. Restart your Flask application

### STEP 4: Test It

Run this to test:
```bash
python test_email.py
```

If you see ✅ SUCCESS, emails are working!

## Quick Links

- Enable 2-Step Verification: https://myaccount.google.com/security
- App Passwords (after 2-Step is enabled): https://myaccount.google.com/apppasswords

## Important Notes

- ✅ Booking approvals still work even if email fails
- ✅ You need 2-Step Verification enabled first
- ✅ App Passwords only work after 2-Step Verification
- ✅ The 16-character password is different from your regular password

## Current Status

- Email: chutiyaabhiram@gmail.com ✅
- 2-Step Verification: Needs to be enabled ❌
- App Passwords: Will be available after enabling 2-Step ✅

Once you enable 2-Step Verification, App Passwords will become available!

