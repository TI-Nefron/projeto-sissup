import uuid
from django.db import models

class Clinic(models.Model):
    """
    Represents a clinic or business unit within the group.
    This is the core of the multi-tenancy data separation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Nome da Clínica", max_length=100, unique=True)
    is_active = models.BooleanField("Ativa", default=True)

    class Meta:
        verbose_name = "Clínica"
        verbose_name_plural = "Clínicas"
        ordering = ['name']

    def __str__(self):
        return self.name