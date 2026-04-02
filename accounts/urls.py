from django.contrib import admin
from django.urls import path,include
from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
import uuid


urlpatterns = [
    path('api/user/register/',UserCreate.as_view(),name='create_user'),
    path('api/token/',TokenObtainPairView.as_view(),name='token_pair_view'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

   
    path('api/auth/user/',UserDetailView.as_view(),name='user-detail'),
    path('api/auth/user/<uuid:pk>/',UserDetailView.as_view(),name='user-detail'),
    path('api/google/validate_token/',validate_google_token,name='validate_token'),
     path('api/google/refresh/token/',Refresh_Google_Access,name='google_refresh_token'),
]
