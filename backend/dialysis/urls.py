from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'dialysis'

router = DefaultRouter()
router.register(r'pacientes', views.PatientViewSet, basename='paciente')

urlpatterns = [
    path('', include(router.urls)),
]