from django.test import TestCase
from rest_framework.exceptions import ValidationError
from app.models.post_model import Post
from app.models.like_model import Like
from django.contrib.auth.models import User
from app.serializers.user_serializer import UserSerializer
from app.serializers.post_serializer import PostSerializer


class TestUserSerializer(TestCase):

    def test_create_user(self):
        # Test for user creation through serializer
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # Check if the data is valid
        user = serializer.save()  # Create the user
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))  # Ensure password is hashed correctly

    def test_invalid_user_data(self):
        # Test for invalid user data (missing password)
        data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        serializer = UserSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)  # Should raise a validation error


class TestPostSerializer(TestCase):

    def setUp(self):
        # Create a user and a post for testing
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.post = Post.objects.create(title='Test Post', content='This is a test post', owner=self.user)

    def test_post_serializer(self):
        # Test if PostSerializer works as expected
        serializer = PostSerializer(self.post)
        self.assertEqual(serializer.data['id'], self.post.id)
        self.assertEqual(serializer.data['title'], self.post.title)
        self.assertEqual(serializer.data['content'], self.post.content)
        self.assertEqual(serializer.data['owner_username'], self.user.username)
        self.assertEqual(serializer.data['likes_count'], 0)  # Since no likes yet

    def test_post_serializer_with_likes(self):
        # Test if likes_count works when there are likes
        like = Like.objects.create(user=self.user, post=self.post)  # Create a like for the post
        self.post.likes.add(like)
        serializer = PostSerializer(self.post)
        self.assertEqual(serializer.data['likes_count'], 1)  # The likes count should be 1


