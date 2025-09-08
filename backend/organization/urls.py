from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'organization'

router = DefaultRouter()
router.register(r'clinics', views.ClinicViewSet, basename='clinic')

urlpatterns = [
    path('', include(router.urls)),
]
