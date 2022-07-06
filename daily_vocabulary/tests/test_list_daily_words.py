from datetime import datetime, timedelta
from django.test import Client, TestCase
from pytz import timezone as py_timezone
from unittest.mock import patch

from ..models import User, Word
from ..utils.utils import calculate_new_score

URL = '/words/daily/'


NOW = datetime(2010, 1, 1, 12, tzinfo=py_timezone('UTC'))

class TestCeateUser(TestCase):
    def setUp(self):
        self.client = Client()

        self.username = 'user'
        password = 'Password123_'
        user = User(
            username=self.username, 
            password=password, 
            email='user@gmail.com',
            timezone=py_timezone('UTC'))
        user.set_password(password)
        user.save()
        self.user = user

        authentification_payload = {
            'username': self.username,
            'password': password
        }
        response = self.client.post('/token/', authentification_payload)
        self.access_token = response.json()['access']

    def __create_example_word(self, created_at_local, original_word='original_word', translated_word='translated_word'):
        word = Word(
            user=self.user, 
            original_word=original_word, 
            translated_word=translated_word, 
            created_at_local=created_at_local)
        word.save()

        return word.id

    def test_do_not_return_word_when_it_was_created_on_the_same_day(self):
        self.__create_example_word(NOW - timedelta(hours=1))

        with patch('daily_vocabulary.views.timezone.now', return_value=NOW):
            response = self.client.get(URL, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_return_when_word_was_created_on_previous_day(self):
        word_id = self.__create_example_word(NOW - timedelta(days=1))

        with patch('daily_vocabulary.views.timezone.now', return_value=NOW):
            response = self.client.get(URL, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['id'], word_id)
