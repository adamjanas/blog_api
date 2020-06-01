from rest_framework import serializers
from api.blog.models import (
    Post,
    Category,
    Comment,
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'category', 'date_posted']


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Post.objects.all())
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_date']
