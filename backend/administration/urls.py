from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    ClinicViewSet,
    GuideTypeViewSet,
    ProcedureStatusViewSet,
    ExitTypeViewSet,
    RoleViewSet,
    ClinicMandatoryDocumentsView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clinics', ClinicViewSet)
router.register(r'guide-types', GuideTypeViewSet)
router.register(r'procedure-statuses', ProcedureStatusViewSet)
router.register(r'exit-types', ExitTypeViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('clinics/<uuid:clinic_id>/mandatory-documents/', ClinicMandatoryDocumentsView.as_view(), name='clinic-mandatory-documents'),
    path('', include(router.urls)),
]
