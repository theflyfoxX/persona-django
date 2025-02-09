from django.contrib import admin
from django.contrib import admin
from .models.like_model import Like
from .models.post_model import Post

# Register the model
admin.site.register(Like)
admin.site.register(Post)
