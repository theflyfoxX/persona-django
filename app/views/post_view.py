from rest_framework import generics, permissions
from app.models.post_model import Post
from app.serializers.post_serializer import PostSerializer

# Get all posts (only authenticated users)
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')  # Order by newest
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can access

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Set the owner to the logged-in user

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.owner:
            raise PermissionError("You are not the owner of this post!")
        serializer.save()
    
    def perform_destroy(self, instance):
        if self.request.user != instance.owner:
            raise PermissionError("You are not allowed to delete this post!")
        instance.delete()
