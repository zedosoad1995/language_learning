from datetime import datetime
from pytz import timezone


def get_days_since(current_date, last_date):
    last_date = last_date.replace(second=0, microsecond=0)

    current_date = current_date.replace(second=0, microsecond=0)

    return int((current_date - last_date).total_seconds() / 60.0)


def tz_diff(tz):
    '''
    Returns the difference in hours between a timezone and UTC, for the current date
    '''
    utc = timezone('UTC')

    now = datetime.now()
    now_tz = utc.localize(now)
    now_utc = tz.localize(now).astimezone(utc)

    return -(now_utc - now_tz).seconds//3600 if now_utc > now_tz else (now_tz - now_utc).seconds//3600