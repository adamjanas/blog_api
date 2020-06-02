from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from django_filters.views import object_filter
from api.blog.models import Post
from api.blog.views import (
        PostViewSet,
        CategoryViewSet,
        CommentViewSet,
)
router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('categories', CategoryViewSet, basename='categories')
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = router.urls
