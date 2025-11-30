# Simple Email Setup Guide - English

## Current Situation

- Your email: **chutiyaabhiram@gmail.com** ✅
- App Passwords page shows error ❌
- Solution: Enable 2-Step Verification first

## Quick Fix (5 Minutes)

### What You Need to Do:

**1. Enable 2-Step Verification**
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow the steps (verify phone number)
   - Turn it ON

**2. Then Get App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Now it will work!
   - Generate password for "Mail"
   - Copy the 16-character password

**3. Update config.py**
   - Open `config.py`
   - Change line 14 to use your App Password
   - Save and restart

## Why This Error?

Google requires 2-Step Verification to be enabled before you can use App Passwords. This is for security.

## Once Done

- Emails will send automatically when you approve bookings
- Users will receive beautiful HTML emails
- Room details included in email

## Need Help?

The system will work even without email - bookings still get approved. Email is just a bonus feature for notifications.

