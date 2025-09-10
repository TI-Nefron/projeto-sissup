from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'dialysis'

router = DefaultRouter()
router.register(r'pacientes', views.PatientViewSet, basename='paciente')
router.register(r'historico', views.PatientHistoryViewSet, basename='historico')
router.register(r'tipos-de-saida', views.ExitTypeViewSet, basename='tipo-de-saida')

urlpatterns = [
    path('', include(router.urls)),
    path('clinics/<uuid:clinic_id>/exit-types/', views.ClinicExitTypeListView.as_view(), name='clinic-exit-types'),
]