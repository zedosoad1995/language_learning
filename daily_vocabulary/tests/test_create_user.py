import ast
from django.test import Client, TestCase

from django import setup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "language_learning.settings")
setup()

from ..models import User

URL = '/users/'

STANDARD_PAYLOAD = {
    'username': 'user',
    'password': 'password',
    'email': 'email@email.com',
    'first_name': 'name',
    'last_name': 'other name',
    'timezone': 'UTC',
    'num_daily_words': 3,
}


class TestCeateUser(TestCase):
    def setUp(self):
        self.client = Client()

    def test_returns_201_when_user_is_created(self):
        response = self.client.post(URL, STANDARD_PAYLOAD, content_type='application/json')

        #print(User.objects.all())

        self.assertEqual(response.status_code, 201)

    def test_returns_404_when_num_of_daily_words_is_invalid(self):
        payload = STANDARD_PAYLOAD
        payload['num_daily_words'] = 4

        response = self.client.post(URL, payload, content_type='application/json')

        constent = ast.literal_eval(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('num_daily_words', constent)
        

