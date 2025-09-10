from .models import AuditLog, log_change

class AuditableSerializerMixin:
    def create(self, validated_data):
        instance = super().create(validated_data)
        log_change(
            user=self.context['request'].user,
            instance=instance,
            action=AuditLog.Action.CREATE,
            changes={'state': self.to_representation(instance)}
        )
        return instance

    def update(self, instance, validated_data):
        before_data = self.to_representation(instance)

        updated_instance = super().update(instance, validated_data)

        after_data = self.to_representation(updated_instance)

        changes = {}
        for key, new_value in after_data.items():
            old_value = before_data.get(key)
            # Compare primitive values
            if old_value != new_value:
                changes[key] = {
                    'old': old_value,
                    'new': new_value
                }
        
        if changes:
            log_change(
                user=self.context['request'].user,
                instance=updated_instance,
                action=AuditLog.Action.UPDATE,
                changes=changes
            )
        return updated_instance

class AuditableViewSetMixin:
    def perform_destroy(self, instance):
        log_change(
            user=self.request.user,
            instance=instance,
            action=AuditLog.Action.DELETE,
            changes={'deleted': self.get_serializer(instance).data}
        )
        instance.delete()
