from django.test import Client, TestCase

from ..models import User

URL = '/users/me/'


class TestCeateUser(TestCase):
    def setUp(self):
        self.client = Client()

        self.username = 'user'
        password = 'Password123_'
        user = User(username=self.username, password=password, email='user@gmail.com',)
        user.set_password(password)
        user.save()

        authentification_payload = {
            'username': self.username,
            'password': password
        }
        response = self.client.post('/token/', authentification_payload)
        self.access_token = response.json()['access']

    def test_edits_logged_user_email(self):
        new_email = 'new_user_email@gmail.com'

        response = self.client.patch(
            URL,
            {'email': new_email},
            content_type='application/json', 
            HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        logged_user = User.objects.filter(username=self.username)[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(logged_user.email, new_email)

    def test_returns_400_when_invalid_email_is_edited(self):
        new_email = 'invalid@invalid'

        response = self.client.patch(
            URL,
            {'email': new_email},
            content_type='application/json', 
            HTTP_AUTHORIZATION=f'JWT {self.access_token}')

        self.assertEqual(response.status_code, 400)        
