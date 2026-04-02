from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Invitation
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GenerateInviteLink(request):
    user = request.user
    company = user.company
    
    if user.role != 'admin':
        return JsonResponse({"Only admins are allowed!"})
    invite = Invitation.objects.create(
        company=company,
        created_by= user,
        expires_at=now()+timedelta(hours=24)
    )
    
    link = invite.token
    
    return JsonResponse({
        "invite_link":link
    })
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_with_invite(request,inviteLink):
    
    user = request.user
    try:
        invite = Invitation.objects.get(token=inviteLink)

        if invite.is_used or invite.expires_at < now():
            return JsonResponse({"error": "Invalid or expired"}, status=400)
        if user.company:
            return JsonResponse({"error": "User already in a company"}, status=400)


        user.company=invite.company
        user.role = 'member'
        user.save()
    

        invite.is_used = True
        invite.save()
        
        return JsonResponse({
            "message":"success at registring company using invite link",
            
        })

        

    except Invitation.DoesNotExist:
        return JsonResponse({"error": "Invalid link"}, status=404)
    
    
    
