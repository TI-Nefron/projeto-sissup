from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'parameters'

router = DefaultRouter()
router.register(r'guide-types', views.GuideTypeViewSet, basename='guidetype')
router.register(r'procedure-statuses', views.ProcedureStatusViewSet, basename='procedurestatus')

urlpatterns = [
    path('', include(router.urls)),
]
