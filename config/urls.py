"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from accounts.views import google_login_callback



from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        "status": "ok",
        "message": "Service is healthy"
    })


urlpatterns = [
    
    path('admin/dj-redis-panel',include("dj_redis_panel.urls")),
    
    # path('admin/dj-celery-panel',include("dj_celery_panel.urls")),
    path('admin/dj-control-room',include("dj_control_room.urls")),
    path('admin/', admin.site.urls),
    path('users/',include('accounts.urls')),
     path('callback/',google_login_callback),
    
    path('accounts/',include('allauth.urls')),  # need to add for allauth
    path('api/auth/',include('rest_framework.urls')),
    
    path('company/',include('companies.urls')),
    path('documents/',include("documents.urls")),
    
    path("ai/",include("ai.urls")),
    path('invitations/',include('invitations.urls')),
    
       path("health/", health_check),
]
