# 🚀 QUICK FIX: Enable Gmail Email System

## The Problem
Your email is failing because Gmail requires an **App Password**, not your regular password.

## ✅ Quick Solution (5 Minutes)

### Step 1: Create Gmail App Password

1. **Go directly to this link:**
   👉 https://myaccount.google.com/apppasswords

2. **If you see a message to enable 2-Step Verification:**
   - Click "Enable" 
   - Follow the steps to enable it
   - Then come back to App Passwords page

3. **Generate App Password:**
   - Select **App**: `Mail`
   - Select **Device**: `Other (Custom name)`
   - Type: `IGNITRON`
   - Click **Generate**

4. **Copy the password:**
   - You'll see a 16-character password like: `abcd efgh ijkl mnop`
   - **Copy it immediately** (you can't see it again!)

### Step 2: Update Your Config

**Option A: Edit config.py directly**

Open `config.py` and change line 14:
```python
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'YOUR-16-CHAR-APP-PASSWORD-HERE'
```
(Remove spaces from the password when pasting)

**Option B: Use the setup script**

Run:
```bash
python setup_gmail_password.py
```

### Step 3: Test It

Run:
```bash
python test_email.py
```

If you see ✅ SUCCESS, you're all set!

## Current Configuration

- ✅ Email: `chutiyaabhiram@gmail.com` (configured)
- ❌ Password: Needs App Password (currently using regular password which won't work)

## Alternative: Use Environment Variable

**PowerShell:**
```powershell
$env:MAIL_PASSWORD="your-16-char-app-password"
python app.py
```

## Need Help?

The email system will:
- ✅ Continue working even if email fails (booking still approved)
- ✅ Show clear error messages in console
- ✅ Not break your application

Once you have the App Password, emails will work automatically!

