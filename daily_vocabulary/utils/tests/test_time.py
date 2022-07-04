import datetime
from django.test import SimpleTestCase
from pytz import timezone as py_timezone

from django import setup
import os

from daily_vocabulary.utils.utils import get_days_since
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "language_learning.settings")
setup()


class TestDaysDifference(SimpleTestCase):
    def test_small_minute_difference_different_day_same_timezone_return_1_day_diff(self):
        current_date = datetime.datetime(2010, 1, 1, 0, 0, 1)
        last_date = datetime.datetime(2009, 12, 31, 23, 59, 59)
        days = get_days_since(current_date, last_date)

        self.assertEqual(days, 1)

    def test_same_day_same_timezone_return_0_days_diff(self):
        current_date = datetime.datetime(2009, 12, 31, 23, 59, 59)
        last_date = datetime.datetime(2009, 12, 31, 0, 0, 0)
        days = get_days_since(current_date, last_date)

        self.assertEqual(days, 0)

    def test_diff_day_on_diff_timezones_but_same_day_on_same_timezone_return_1_day_diff(self):
        # (2009, 12, 31, 23, 30) America/New_York -> (2010, 1, 1, 5, 30, 0) UTC = 1 day

        # (2009, 12, 31, 23, 30) America/New_York = (2010, 1, 1, 4, 30) UTC
        last_date = datetime.datetime(2009, 12, 31, 23, 30, tzinfo=py_timezone('America/New_York'))
        current_date = datetime.datetime(2010, 1, 1, 5, 30, tzinfo=py_timezone('UTC'))

        days = get_days_since(current_date, last_date)

        self.assertEqual(days, 1)

    def test_same_day_on_diff_timezones_but_diff_day_on_same_timezone_return_0_days_diff(self):
        # (2010, 1, 1, 6, 30) Asia/Bangkok -> (2010, 1, 1, 0, 0, 0) UTC = 0 days

        # (2010, 1, 1, 6, 30) Asia/Bangkok = (2009, 12, 31, 23, 30) UTC
        last_date = datetime.datetime(2010, 1, 1, 6, 30, tzinfo=py_timezone('Asia/Bangkok'))
        current_date = datetime.datetime(2010, 1, 1, 0, 0, 0, tzinfo=py_timezone('UTC'))

        days = get_days_since(current_date, last_date)

        self.assertEqual(days, 0)