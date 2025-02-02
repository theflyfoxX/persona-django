from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import User
from django.test import TestCase



class TestUserViews(APITestCase):

    def setUp(self):
        # This method will run before every test, ensuring a fresh user is created
        self.username = f'testuser_{uuid.uuid4()}'
        self.password = 'password123'
        self.email = 'test@example.com'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': f'testuser_{uuid.uuid4()}',
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)  # Should return the access token

    def test_login_user(self):
        username = self.user.username  # Get the user from the register test
        url = reverse('login')
        data = {
            'username': username,
            'password': 'password123'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Should return the access token
        return response.data['access']  # Return the access token

    def test_user_list(self):
        url = reverse('get_all_users')
        access_token = self.test_login_user()  # Get token from login method
        
        # Add token to Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
        # Now make the request to the protected view
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return only one user

    def test_user_detail(self):
        url = reverse('get_user_by_id', kwargs={'id': self.user.id})
        access_token = self.test_login_user()  # Get token from login method
        
        # Add token to Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
        # Now make the request to the protected view
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)  # Sh
