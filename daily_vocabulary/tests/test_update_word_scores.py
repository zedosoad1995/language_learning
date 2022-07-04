from datetime import datetime, timedelta
from django.test import Client, TestCase
from pytz import timezone as py_timezone
from unittest.mock import patch

from django import setup
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "language_learning.settings")
setup()

from ..models import User, Word
from ..utils.utils import calculate_new_score

URL = '/words/update/'


class TestCeateUser(TestCase):
    def setUp(self):
        self.client = Client()

        self.username = 'user'
        password = 'Password123_'
        self.past_update = datetime(2020, 1, 1, tzinfo=py_timezone('UTC'))
        user = User(
            username=self.username, 
            password=password, 
            email='user@gmail.com',
            last_update=self.past_update,
            timezone=py_timezone('UTC'))
        user.set_password(password)
        user.save()

        authentification_payload = {
            'username': self.username,
            'password': password
        }
        response = self.client.post('/token/', authentification_payload)
        self.access_token = response.json()['access']

        word = Word(
            user=user, 
            original_word='original_word', 
            translated_word='translated_word', 
            created_at_local=self.past_update - timedelta(days=600))
        word.save()
        self.word_id = word.id

    def test_do_not_update_when_last_update_was_made_in_same_day(self):
        with patch('daily_vocabulary.views.timezone.now', return_value=self.past_update + timedelta(hours=1)):
            response = self.client.post(URL, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        logged_user = User.objects.filter(username=self.username).first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(logged_user.last_update, self.past_update)

    def test_update_word_score_by_number_of_days_passed_since_last_update(self):
        days_since_last_update = 2

        with patch('daily_vocabulary.views.timezone.now', return_value=self.past_update + timedelta(days=days_since_last_update)):
            response = self.client.post(URL, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        word = Word.objects.filter(id=self.word_id).first()
        self.assertEqual(word.score, calculate_new_score(days_since_last_update, word.relevance, word.knowledge))
        self.assertEqual(response.status_code, 200)
