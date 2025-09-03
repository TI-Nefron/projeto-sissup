from django.urls import path
from . import views

app_name = 'dialysis'

urlpatterns = [
    path('reception/search/', views.patient_search_view, name='patient_search'),
    path('patient/<uuid:patient_id>/checklist/', views.patient_checklist_view, name='patient_checklist'),
]