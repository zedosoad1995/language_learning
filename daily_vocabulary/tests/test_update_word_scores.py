from datetime import datetime, timedelta
from django.test import Client, TestCase
from pytz import timezone as py_timezone
from unittest.mock import patch

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

        self.assertEqual(logged_user.last_update, self.past_update)
        self.assertEqual(response.status_code, 200)

    def test_update_word_score_by_number_of_days_passed_since_last_update(self):
        days_since_last_update = 2

        with patch('daily_vocabulary.views.timezone.now', return_value=self.past_update + timedelta(days=days_since_last_update)):
            response = self.client.post(URL, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        word = Word.objects.filter(id=self.word_id).first()
        self.assertEqual(word.score, calculate_new_score(days_since_last_update, word.relevance, word.knowledge))
        self.assertEqual(response.status_code, 200)

    def test_update_word_score_to_zero_if_word_was_seen(self):
        word = Word.objects.filter(id=self.word_id).first()
        word.is_seen = True
        word.save()

        with patch('daily_vocabulary.views.timezone.now', return_value=self.past_update + timedelta(days=3)):
            response = self.client.post(URL, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        word = Word.objects.filter(id=self.word_id).first()
        self.assertEqual(word.score, 0)
        self.assertEqual(word.is_seen, False)
        self.assertEqual(response.status_code, 200)

    def test_update_by_number_of_says_since_word_creation_when_it_happened_after_last_update(self):
        word_update_days_after = 2
        current_update_days_after = 3

        word = Word.objects.filter(id=self.word_id).first()
        word.created_at_local = self.past_update + timedelta(days=word_update_days_after)
        word.save()

        with patch('daily_vocabulary.views.timezone.now', return_value=self.past_update + timedelta(days=current_update_days_after)):
            response = self.client.post(URL, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        word = Word.objects.filter(id=self.word_id).first()
        self.assertEqual(word.score, calculate_new_score(current_update_days_after - word_update_days_after, word.relevance, word.knowledge))
        self.assertEqual(response.status_code, 200)

    def test_update_word_score_once_when_trying_to_update_multiple_times_in_the_same_day(self):
        days_after_prev_update = 1

        for mins in range(0, 3):
            with patch('daily_vocabulary.views.timezone.now', return_value=self.past_update + timedelta(days=days_after_prev_update, minutes=mins)):
                self.client.post(URL, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        word = Word.objects.filter(id=self.word_id).first()
        self.assertEqual(word.score, calculate_new_score(1, word.relevance, word.knowledge))

    def test_update_once_when_user_ping_pongs_diff_timezones_to_try_to_change_the_day_multiple_times(self):
        days_after_prev_update = 1

        with patch('daily_vocabulary.views.timezone.now', return_value=self.past_update + timedelta(days=days_after_prev_update, minutes=0)):
            self.client.post(URL, {'timezone': 'UTC'}, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')
        
        with patch('daily_vocabulary.views.timezone.now', return_value=self.past_update + timedelta(days=days_after_prev_update, minutes=1)):
            self.client.post(URL, {'timezone': 'America/New_York'}, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        with patch('daily_vocabulary.views.timezone.now', return_value=self.past_update + timedelta(days=days_after_prev_update, minutes=2)):
            self.client.post(URL, {'timezone': 'UTC'}, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        word = Word.objects.filter(id=self.word_id).first()
        self.assertEqual(word.score, calculate_new_score(1, word.relevance, word.knowledge))

        logged_user = User.objects.filter(username=self.username).first()
        self.assertEqual(logged_user.last_update, self.past_update + timedelta(days=days_after_prev_update))

    def test_returns_400_when_invalid_timezone_in_payload(self):
        invalid_timezone = 'invalid'

        with patch('daily_vocabulary.views.timezone.now', return_value=self.past_update):
            response = self.client.post(URL, {'timezone': invalid_timezone}, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        self.assertEqual(response.status_code, 400)
        