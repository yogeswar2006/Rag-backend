from .views import DocumentsView
from django.urls import path

urlpatterns = [
    path('upload/document/', DocumentsView.as_view(), name="documents"),
]