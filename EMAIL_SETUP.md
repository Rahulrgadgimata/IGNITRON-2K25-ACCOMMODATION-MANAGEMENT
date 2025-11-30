# Email Configuration Guide for IGNITRON 2K25

## Setup Instructions

### 1. Install Required Packages

```bash
pip install -r requirements.txt
```

### 2. Configure Gmail Credentials

You have **two options** to configure your Gmail credentials:

#### Option A: Using Environment Variables (Recommended)

Set these environment variables:

**Windows (PowerShell):**
```powershell
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="your-app-password"
```

**Windows (Command Prompt):**
```cmd
set MAIL_USERNAME=your-email@gmail.com
set MAIL_PASSWORD=your-app-password
```

**Linux/Mac:**
```bash
export MAIL_USERNAME="your-email@gmail.com"
export MAIL_PASSWORD="your-app-password"
```

#### Option B: Using .env File

1. Run the setup script:
```bash
python setup_email.py
```

2. Or create a `.env` file manually in the project root:
```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 3. Create Gmail App Password

**Important:** Gmail requires an App Password, not your regular password!

#### Steps to Create Gmail App Password:

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click on **Security** (left sidebar)
3. Enable **2-Step Verification** (if not already enabled)
4. Scroll down and click on **App passwords**
5. Select **Mail** as the app and **Other (Custom name)** as device
6. Enter "IGNITRON Accommodation" as the custom name
7. Click **Generate**
8. Copy the 16-character password (it will look like: `abcd efgh ijkl mnop`)
9. Use this password in your configuration (without spaces)

### 4. Update Config Directly (Alternative)

You can also edit `config.py` directly:

```python
class Config:
    # ... other config ...
    MAIL_USERNAME = 'your-email@gmail.com'
    MAIL_PASSWORD = 'your-app-password-here'
```

### 5. Test Email Configuration

After setting up, restart your Flask application:

```bash
python app.py
```

When you approve a booking, an email will be automatically sent to the user.

## Email Features

- ✅ **Automatic Email on Approval**: Users receive email when booking is approved
- ✅ **Room Details Included**: Email contains room number and description
- ✅ **Professional HTML Design**: Beautiful, responsive email template
- ✅ **Error Handling**: Application continues even if email fails

## Troubleshooting

### Email not sending?

1. **Check App Password**: Make sure you're using App Password, not regular password
2. **Check 2-Step Verification**: App passwords only work if 2-Step Verification is enabled
3. **Check Credentials**: Verify MAIL_USERNAME and MAIL_PASSWORD are set correctly
4. **Check Console**: Look for error messages in the terminal
5. **Check Gmail Security**: Some accounts may need to allow "Less secure app access" (not recommended, use App Password instead)

### Common Errors

- **"Authentication failed"**: Wrong password or not using App Password
- **"Connection refused"**: Firewall or network issue
- **"Username and Password not accepted"**: Use App Password, not regular password

## Security Notes

- ⚠️ **Never commit your credentials** to version control
- ✅ `.env` file is already in `.gitignore`
- ✅ Use environment variables for production
- ✅ App Passwords are safer than enabling "Less secure app access"

## Email Template

The email includes:
- Room allocation details
- Room number and description
- Booking status
- Check-in instructions
- Link to user dashboard
- Professional Ignitron branding

## Support

If you encounter any issues, check:
1. Python console output for error messages
2. Email service logs
3. Gmail account security settings


