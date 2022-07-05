from django.test import Client, TestCase

from ..models import User

URL = '/users/me/'


class TestCeateUser(TestCase):
    def setUp(self):
        self.client = Client()

        self.username = 'user'
        password = 'Password123_'
        user = User(username=self.username, password=password, email='user@gmail.com')
        user.set_password(password)
        user.save()

        authentification_payload = {
            'username': self.username,
            'password': password
        }
        response = self.client.post('/token/', authentification_payload)
        self.access_token = response.json()['access']

    def test_returns_logged_user_when_correctly_authentificated(self):
        response = self.client.get(URL, content_type='application/json', HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], self.username)
