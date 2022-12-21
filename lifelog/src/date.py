from dateutil.relativedelta import relativedelta
from dateutil.utils import within_delta
from dateutil.parser import parse
from datetime import datetime
from datetime import timedelta

def epoch_to_iso(epoch: str) -> str:
    """Convert UNIX timestamp to ISO 8601 date"""
    return datetime.fromtimestamp(float(epoch)).isoformat()

def iso_to_date(iso_date: str) -> str:
    """Convert ISO 8601 date to a human readable date"""
    # YYYY-MM-DD HH-MM-SS (24-HR format)
    return parse(iso_date).strftime('%Y-%m-%d %H:%M:%S') 

def within_six_months(date1: str, date2: str) -> bool:
    """Check if the dates are within six months"""
    return within_delta(parse(date1), parse(date2), timedelta(days=_days(parse(date1))))

def _days(date: datetime) -> int:
    """Get the number of days from six months ago"""
    return abs(date - (date + relativedelta(months=-6))).days
