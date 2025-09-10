from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentUploadView, DocumentTypeViewSet

app_name = 'documents'

router = DefaultRouter()
router.register(r'document-types', DocumentTypeViewSet)

urlpatterns = [
    path('documents/upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('', include(router.urls)),
]