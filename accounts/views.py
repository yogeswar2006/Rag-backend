
from django.shortcuts import redirect
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from allauth.socialaccount.models import SocialAccount,SocialToken
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response

load_dotenv()
import os

import json

# Create your views here.

User = get_user_model()

class UserCreate(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[AllowAny]

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        return self.request.user

@login_required
def google_login_callback(request):
    user=request.user
    social_accounts=SocialAccount.objects.filter(user=user)
    # print("social accounts for user",social_accounts)
    
    social_account=social_accounts.first()
    
    if not social_account:
        return redirect('http://localhost:5173/login/callback/?error=NoSocialAccount')
    
    token = SocialToken.objects.filter(account=social_account,account__provider='google').first()
    if token:
        print("Google Token found ",token.token)
        refresh=RefreshToken.for_user(user)
        access_token  = str(refresh.access_token)
        return redirect(f'http://localhost:5173/login/callback/?access_token={access_token}')
    else:
        print("No google token found for user ",user)
        return redirect('http://localhost:5173/login/callback/?error=NoGoogleToken')

@csrf_exempt
def validate_google_token(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            google_token=data.get('access_token')
            print(google_token)
            if not google_token:
                return JsonResponse({"detail":"access token is missing"},status=400)
            return JsonResponse({"valid":"True"})
        except json.JSONDecodeError:
            return JsonResponse({"detail":"Invalid Json"},status=400)
    return JsonResponse({"detail":"Method not alowed"},ststus=405)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Refresh_Google_Access(request):
    user = request.user
    token = SocialToken.objects.get(account__user=user)
    refresh_token = token.token_secret
    
    data={
        "client_id": os.getenv('OAUTH_CLIENT_ID'),
        "client_secret": os.getenv('OAUTH_SECRECT_KEY'),
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    URL="https://oauth2.googleapis.com/token"
    
    res = requests.post(URL,data=data)
    
    return Response(res.json())
    
    