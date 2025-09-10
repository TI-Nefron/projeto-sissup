from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'billing'

router = DefaultRouter()
router.register(r'guias', views.GuideViewSet, basename='guia')
router.register(r'payers', views.PayerViewSet, basename='payer')

urlpatterns = [
    path('', include(router.urls)),
    path('clinics/<uuid:clinic_id>/payers/', views.ClinicPayerListView.as_view(), name='clinic-payers'),
]
