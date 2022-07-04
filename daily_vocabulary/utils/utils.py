from datetime import datetime
from pytz import timezone


def get_days_since(current_date, last_date):
    # minutes since
    """ last_date = last_date.replace(second=0, microsecond=0)
    current_date = current_date.replace(second=0, microsecond=0)

    return int((current_date - last_date).total_seconds() / 60.0) """

    last_date = last_date.replace(hour=0, minute=0, second=0, microsecond=0)
    current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)

    return int((current_date.replace(tzinfo=None) - last_date.replace(tzinfo=None)).total_seconds() / (60 * 60 * 24))
    

def calculate_new_score(days_since, relevance, knowledge):
    return days_since * (relevance + 6 - knowledge)