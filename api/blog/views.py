from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from api.core.mixins import ActionPermissionMixin
from api.core.permissions import IsAuthor, MyUserPermissions
from django_filters import rest_framework as filters
from rest_framework import mixins
from api.blog.serializers import (
    PostSerializer,
    CategorySerializer,
    CommentSerializer,
)
from api.blog.models import (
    Post,
    Category,
    Comment,
)


class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    date_posted = filters.NumberFilter(lookup_expr='iexact')
    date_posted_lt = filters.NumberFilter(lookup_expr='lte', label='Date posted is less than')
    date_posted_gt = filters.NumberFilter(lookup_expr='gte', label='Date posted is greater than')

    class Meta:
        model = Post
        fields = ('title', 'category', 'date_posted')


class PostViewSet(ActionPermissionMixin, viewsets.ModelViewSet):
    permission_classes_by_action = {
        "default": (IsAuthenticated,),
        "update": (IsAuthor,),
        "partial_update": (IsAuthor,),
        "destroy": (IsAuthor,),
    }
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CommentViewSet(ActionPermissionMixin, viewsets.ModelViewSet):
    permission_classes_by_action = {
        "default": (IsAuthenticated,),
        "update": (IsAuthor,),
        "partial_update": (IsAuthor,),
        "destroy": (IsAuthor,),
    }
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
