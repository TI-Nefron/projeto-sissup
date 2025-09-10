from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'audit'

router = DefaultRouter()
router.register(r'logs', views.AuditLogViewSet, basename='auditlog')

urlpatterns = [
    path('', include(router.urls)),
    path('content-type/', views.ContentTypeView.as_view(), name='content-type'),
]
