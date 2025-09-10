from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'parameters'

router = DefaultRouter()
router.register(r'guide-types', views.GuideTypeViewSet, basename='guidetype')
router.register(r'procedure-statuses', views.ProcedureStatusViewSet, basename='procedurestatus')

urlpatterns = [
    path('', include(router.urls)),
    path('clinics/<uuid:clinic_id>/guide-types/', views.ClinicGuideTypeListView.as_view(), name='clinic-guide-types'),
    path('clinics/<uuid:clinic_id>/procedure-statuses/', views.ClinicProcedureStatusListView.as_view(), name='clinic-procedure-statuses'),
]
