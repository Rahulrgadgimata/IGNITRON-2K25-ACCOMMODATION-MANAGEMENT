# ⚠️ IMPORTANT: Gmail App Password Required

Your Gmail account requires an **App Password** instead of your regular password.

## Quick Steps to Create Gmail App Password:

### Step 1: Enable 2-Step Verification
1. Go to: https://myaccount.google.com/security
2. Click on **2-Step Verification**
3. Follow the steps to enable it (if not already enabled)

### Step 2: Generate App Password
1. Still on the Security page, scroll down
2. Look for **"App passwords"** section
3. Click on it (or go to: https://myaccount.google.com/apppasswords)
4. Select **"Mail"** as the app
5. Select **"Other (Custom name)"** as device
6. Type: **"IGNITRON Accommodation"**
7. Click **"Generate"**
8. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)

### Step 3: Update Configuration

After you get the App Password, update it in `config.py`:

```python
MAIL_PASSWORD = 'your-16-character-app-password-here'  # Remove spaces
```

**OR** set it as environment variable:

**PowerShell:**
```powershell
$env:MAIL_PASSWORD="your-16-character-app-password"
```

## Why App Password?

Gmail blocks regular passwords for security. App Passwords are:
- ✅ More secure
- ✅ Specific to each application
- ✅ Can be revoked individually
- ✅ Required when 2-Step Verification is enabled

## Test Your Configuration

After updating with App Password, run:
```bash
python test_email.py
```

You should see: ✅ SUCCESS! Test email sent successfully!

## Current Configuration Status

- ✅ Email: chutiyaabhiram@gmail.com (configured)
- ❌ Password: Needs to be App Password (not regular password)

