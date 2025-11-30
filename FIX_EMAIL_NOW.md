# Fix Email System - Step by Step (English)

## The Problem

When you try to access App Passwords, you see:
**"The setting you are looking for is not available for your account"**

This happens because you need to **enable 2-Step Verification first**.

## Solution: Enable 2-Step Verification First

### Step 1: Enable 2-Step Verification

1. Go to this link:
   👉 **https://myaccount.google.com/security**

2. On the Security page, find the section called:
   **"2-Step Verification"**

3. Click on **"Get Started"** or **"Turn On"** button

4. Follow these steps:
   - Enter your phone number
   - Choose how to verify (SMS text message or phone call)
   - Google will send you a code
   - Enter that code to verify
   - Click "Turn On"

5. Wait for confirmation - 2-Step Verification is now ON

### Step 2: Now Access App Passwords

1. After 2-Step Verification is enabled, go to:
   👉 **https://myaccount.google.com/apppasswords**

2. **Now the page should work!** (No more error)

3. Generate App Password:
   - Select **App**: Mail
   - Select **Device**: Other (Custom name)
   - Type: **IGNITRON**
   - Click **Generate**

4. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)

### Step 3: Update Configuration

1. Open `config.py` file

2. Find line 14 (MAIL_PASSWORD)

3. Replace with your App Password:
   ```python
   MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-16-char-app-password'
   ```
   (Remove spaces when pasting)

4. Save the file

5. Restart your Flask app

### Step 4: Test

Run this command:
```bash
python test_email.py
```

You should see: ✅ SUCCESS!

## Summary

1. ✅ Enable 2-Step Verification first
2. ✅ Then App Passwords will become available
3. ✅ Generate App Password
4. ✅ Update config.py
5. ✅ Test and use!

## Important

- Your email is already configured: chutiyaabhiram@gmail.com
- You just need to enable 2-Step Verification first
- App Passwords only work after 2-Step Verification is enabled
- The booking system works even without email - email is just for notifications

## Need Help?

Check `ENABLE_APP_PASSWORDS_STEPS.md` for more detailed instructions.

