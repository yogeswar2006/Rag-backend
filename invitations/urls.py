from django.urls import path, include
from .views import GenerateInviteLink,register_with_invite

urlpatterns = [
    path("generate/invite/",GenerateInviteLink,name='invite_link'),
    path('company/register/<uuid:inviteLink>/',register_with_invite,name='company_register'),
]
