from parameterized import parameterized
from django.test import Client, TestCase

from django import setup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "language_learning.settings")
setup()

from ..models import User

URL = '/users/'

STANDARD_PAYLOAD = {
    'username': 'user',
    'password': 'Password123_',
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

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(User.objects.all()), 1)
    
    @parameterized.expand([
       ('aa'),
       ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
       ('username!'),
   ])
    def test_returns_400_when_invalid_username_is_given(self, username):
        #payload = {k: v for k, v in STANDARD_PAYLOAD.items() if k != 'password'}
        payload = STANDARD_PAYLOAD.copy()
        payload['username'] = username
        response = self.client.post(URL, payload, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    @parameterized.expand([
       ('password'),
       ('small'),
       ('huuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuge'),
       ('Password123'),
   ])
    def test_returns_400_when_invalid_password_is_given(self, password):
        payload = STANDARD_PAYLOAD.copy()
        payload['password'] = password
        response = self.client.post(URL, payload, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_returns_400_when_num_of_daily_words_is_invalid(self):
        payload = STANDARD_PAYLOAD.copy()
        payload['num_daily_words'] = 4

        response = self.client.post(URL, payload, content_type='application/json')

        self.assertEqual(response.status_code, 400)
