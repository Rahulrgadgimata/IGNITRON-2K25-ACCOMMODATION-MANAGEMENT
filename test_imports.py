#!/usr/bin/env python
"""Test script to verify all imports work correctly"""

try:
    print("Testing imports...")
    import pytz
    print(f"✓ pytz imported successfully (version: {pytz.__version__})")
    
    from models import IST, get_ist_now
    print(f"✓ Models imported successfully")
    print(f"✓ IST timezone: {IST}")
    
    current_time = get_ist_now()
    print(f"✓ Current IST time: {current_time}")
    
    from app import app
    print("✓ Flask app imported successfully")
    print("\n✅ All imports successful! The application should work correctly.")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\nPlease install missing packages:")
    print("  pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error: {e}")

