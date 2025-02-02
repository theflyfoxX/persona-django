from rest_framework import serializers
from app.models.post_model import Post
from app.models.like_model import Like

class PostSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    likes_count = serializers.SerializerMethodField()  # Get total likes

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'owner', 'owner_username', 'likes_count')

    def get_likes_count(self, obj):
        return obj.likes.count()  # Count total likes on the post
