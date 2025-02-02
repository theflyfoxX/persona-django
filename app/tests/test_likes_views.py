from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from app.models.like_model import Like
from app.models.post_model import Post
from rest_framework_simplejwt.tokens import RefreshToken

class TestLikeViews(APITestCase):

    def setUp(self):
        # Create the user and get access token
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Set the authorization header for the client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create a post
        self.post = Post.objects.create(title='Test Post', content='This is a test post', owner=self.user)

    def test_like_post(self):
        url = reverse('like_unlike_post', kwargs={'post_id': self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)  # Ensure like is created

    def test_unlike_post(self):
        # Create a like manually for the post
        Like.objects.create(user=self.user, post=self.post)

        url = reverse('like_unlike_post', kwargs={'post_id': self.post.id})
        response = self.client.post(url)  # Same post, like should be removed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)  # Ensure like is removed

    def test_like_post_already_liked(self):
        # Ensure that like does not create a duplicate
        Like.objects.create(user=self.user, post=self.post)

        url = reverse('like_unlike_post', kwargs={'post_id': self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should toggle the like off
        self.assertEqual(Like.objects.count(), 0)  # Like should be removed

    def test_unauthenticated_user_like_post(self):
        self.client.credentials()  # Log out the user by removing the token
        url = reverse('like_unlike_post', kwargs={'post_id': self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Should return unauthorized

    def test_multiple_likes_not_allowed(self):
        # Ensure a user cannot like the same post multiple times
        Like.objects.create(user=self.user, post=self.post)
        
        url = reverse('like_unlike_post', kwargs={'post_id': self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should toggle the like off
        self.assertEqual(Like.objects.count(), 0)  # Ensure like is removed
