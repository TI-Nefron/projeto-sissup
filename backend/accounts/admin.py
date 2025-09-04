from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    new_fieldsets = list(UserAdmin.fieldsets)
    new_fieldsets.append(
        ('Acesso Multi-Clínica', {'fields': ('clinics',)})
    )
    fieldsets = new_fieldsets

    new_add_fieldsets = list(UserAdmin.add_fieldsets)
    new_add_fieldsets.append(
        (None, {'fields': ('clinics',)})
    )
    add_fieldsets = new_add_fieldsets