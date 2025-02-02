from django.contrib import admin
from django.urls import path
from app.views.user_view import UserListView, UserDetailView, RegisterUserView, CustomLoginView
from app.views.post_view import PostListCreateView, PostDetailView
from app.views.like_view import LikeToggleView
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    
    path('admin/', admin.site.urls),
    # Authentication
    path('api/user/register/', RegisterUserView.as_view(), name='register'),
    path('api/user/login/', CustomLoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User APIs
    path('api/users/', UserListView.as_view(), name='get_all_users'),
    path('api/users/<int:id>/', UserDetailView.as_view(), name='get_user_by_id'),

    # Post APIs
    path('api/posts/', PostListCreateView.as_view(), name='get_all_posts'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='get_update_delete_post'),

    # Like/Unlike API
    path('api/posts/<int:post_id>/like/', LikeToggleView.as_view(), name='like_unlike_post'),
]
