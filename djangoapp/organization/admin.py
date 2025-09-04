from django.contrib import admin
from .models import Clinic

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'cnpj',
        'is_active',
    )
    search_fields = (
        'name',
        'cnpj',
    )
    list_filter = (
        'is_active',
    )
    ordering = ('name',)