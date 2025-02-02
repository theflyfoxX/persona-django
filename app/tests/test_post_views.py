from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from app.models.post_model import Post
from rest_framework_simplejwt.tokens import RefreshToken



class TestPostViews(APITestCase):

    def setUp(self):
        # Create the user
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')

        # Log in to get the access token (if using JWT)
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Set the authorization header for the client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Create a post
        self.post = Post.objects.create(title='Test Post', content='This is a test post', owner=self.user)

    def test_create_post(self):
        url = reverse('get_all_posts')
        data = {
            'title': 'New Post',
            'content': 'This is a new post',
            'owner': self.user.id  # Explicitly passing the owner ID
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)  # Ensure one more post is created

    def test_update_post(self):
        url = reverse('get_update_delete_post', kwargs={'pk': self.post.id})
        data = {
            'title': 'Updated Post',
            'content': 'Updated content',
            'owner': self.user.id  # Explicitly passing the owner ID
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Post')

        # Ensure the post was updated in the database
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')
        self.assertEqual(self.post.content, 'Updated content')

    def test_get_post_detail(self):
        url = reverse('get_update_delete_post', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)

    def test_delete_post(self):
        url = reverse('get_update_delete_post', kwargs={'pk': self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())  # Ensure post is deleted

    def test_create_post_unauthenticated(self):
        self.client.logout()  # Log out the user to simulate unauthenticated access
        url = reverse('get_all_posts')
        data = {'title': 'New Post', 'content': 'This is a new post'}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
