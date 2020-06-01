from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from api.users.serializers import UserSerializer
from django.contrib.auth.models import User


class UserCreate(generics.CreateAPIView):
    """
        create the user
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()


