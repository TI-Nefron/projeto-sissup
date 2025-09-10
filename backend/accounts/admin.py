from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from audit.models import AuditLog, log_change

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

    def save_model(self, request, obj, form, change):
        # Determine action
        action = AuditLog.Action.CREATE if not change else AuditLog.Action.UPDATE

        # Get changes
        changes = {}
        if change and form.changed_data:
            for field_name in form.changed_data:
                changes[field_name] = {
                    'old': form.initial.get(field_name),
                    'new': form.cleaned_data.get(field_name)
                }

        super().save_model(request, obj, form, change)
        log_change(request.user, obj, action, changes)

    def delete_model(self, request, obj):
        log_change(request.user, obj, AuditLog.Action.DELETE)
        super().delete_model(request, obj)