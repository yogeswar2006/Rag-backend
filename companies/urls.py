from .views import CompanyViews
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router  = DefaultRouter()
router.register(r'companies',CompanyViews,basename="companies")

urlpatterns = router.urls 

