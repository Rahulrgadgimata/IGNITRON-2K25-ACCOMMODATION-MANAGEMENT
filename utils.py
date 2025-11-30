from datetime import datetime
import pytz

# Indian Standard Time timezone
IST = pytz.timezone('Asia/Kolkata')

def get_ist_now():
    """Get current time in Indian Standard Time"""
    return datetime.now(IST)

def utc_to_ist(utc_dt):
    """Convert UTC datetime to IST"""
    if utc_dt is None:
        return None
    if utc_dt.tzinfo is None:
        # Assume it's UTC if no timezone info
        utc_dt = pytz.utc.localize(utc_dt)
    return utc_dt.astimezone(IST)

