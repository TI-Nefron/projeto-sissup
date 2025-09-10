from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    ClinicViewSet,
    GuideTypeViewSet,
    ProcedureStatusViewSet,
    ExitTypeViewSet,
    RoleViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clinics', ClinicViewSet)
router.register(r'guide-types', GuideTypeViewSet)
router.register(r'procedure-statuses', ProcedureStatusViewSet)
router.register(r'exit-types', ExitTypeViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
