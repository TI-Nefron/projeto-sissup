
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class Clinic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        _("Nome da Clínica"),
        max_length=100,
        unique=True
    )
    cnpj = models.CharField(
        _("CNPJ"),
        max_length=18,
        unique=True,
        help_text=_("Formato: 00.000.000/0001-00")
    )
    is_active = models.BooleanField(
        _("Ativa"),
        default=True
    )

    mandatory_document_types = models.ManyToManyField(
        'documents.DocumentType',
        verbose_name=_("Tipos de Documentos Obrigatórios"),
        blank=True,
        related_name="mandating_clinics"
    )

    class Meta:
        verbose_name = _("Clínica")
        verbose_name_plural = _("Clínicas")
        ordering = ['name']

    def __str__(self):
        return self.name