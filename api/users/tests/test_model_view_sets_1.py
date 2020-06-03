from django.urls import reverse
from rest_framework.test import APITestCase
from api.users.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token


class UserTest(APITestCase):

    def setUp(self):

        self.credentials = {
            'username': 'testuser1',
            'email': 'test1@email.com',
            'password': 'testpassword1'
        }
        self.test_user = User.objects.create_user(**self.credentials)

        self.create_url = reverse('register')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it
        """
        data = {
            'username': 'testuser2',
            'email': 'test2@email.com',
            'password': 'testpassword2'
        }

        response = self.client.post(self.create_url, data, format='json')

        user = User.objects.latest('id')

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])

        token = Token.objects.get(user=user)

        self.assertEqual(response.data['token'], token.key)

    def test_create_user_with_too_short_password(self):

        data = {
            'username': 'testuser3',
            'email': 'test3@email.com',
            'password': 't'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


    def test_user_with_no_password(self):

        data = {
            'username': 'testuser4',
            'email': 'test4@email.com',
            'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_with_whitespace_password(self):

        data = {
            'username': 'testuser4',
            'email': 'test4@email.com',
            'password': '     '
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_with_too_long_username(self):

        data = {
            'username': 'test'*30,
            'email': 'test5@email.com',
            'password': 'testpassword5'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_with_no_username(self):

        data = {
            'username': '',
            'email': 'test6@email.com',
            'password': 'testpassword6'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_with_existing_username(self):

        data = {
            'username': 'testuser1',
            'email': 'test7@email.com',
            'password': 'testpassword7'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_with_existing_email(self):

        data = {
            'username': 'testuser8',
            'email': 'test1@email.com',
            'password': 'testpassword8'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_with_invalid_email(self):

        data = {
            'username': 'testuser8',
            'email': 'invalid_email',
            'password': 'testpassword8'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_with_no_email(self):

        data = {
            'username': 'testuser9',
            'email': '',
            'password': 'testpassword9'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)