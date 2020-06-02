from django.urls import path
from api.users.views import (
    UserCreate
)

urlpatterns = [
    path('api/users/register', UserCreate.as_view(), name='register'),

]