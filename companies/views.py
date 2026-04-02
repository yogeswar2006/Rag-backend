from django.shortcuts import render
from .serializers import CompanySerializer
from rest_framework.viewsets import ModelViewSet
from .models import Company
# Create your views here.


class CompanyViews(ModelViewSet):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer
    
    