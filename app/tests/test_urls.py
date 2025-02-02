from django.test import SimpleTestCase
from django.urls import resolve, reverse
from app.views.user_view import UserListView, UserDetailView, RegisterUserView, CustomLoginView
from app.views.post_view import PostListCreateView, PostDetailView
from app.views.like_view import LikeToggleView
from rest_framework_simplejwt.views import TokenRefreshView


class TestUrls(SimpleTestCase):

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, RegisterUserView)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)

    def test_token_refresh_url_resolves(self):
        url = reverse('token_refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_get_all_users_url_resolves(self):
        url = reverse('get_all_users')
        self.assertEqual(resolve(url).func.view_class, UserListView)

    def test_get_user_by_id_url_resolves(self):
        url = reverse('get_user_by_id', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, UserDetailView)

    def test_get_all_posts_url_resolves(self):
        url = reverse('get_all_posts')
        self.assertEqual(resolve(url).func.view_class, PostListCreateView)

    def test_get_update_delete_post_url_resolves(self):
        url = reverse('get_update_delete_post', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, PostDetailView)

    def test_like_unlike_post_url_resolves(self):
        url = reverse('like_unlike_post', kwargs={'post_id': 1})
        self.assertEqual(resolve(url).func.view_class, LikeToggleView)
