from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")

def today_ist():
    return datetime.now(IST).date()

def today_str():
    return str(today_ist())
