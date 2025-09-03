import hashlib
import uuid
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from organization.models import Clinic
from billing.models import Guide
from .constants import AllDocumentTypes
from .storages import PatientDocumentStorage, GuideDocumentStorage

def get_document_storage(instance):
    if isinstance(instance.content_object, Guide):
        return GuideDocumentStorage()
    return PatientDocumentStorage()

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    clinic = models.ForeignKey(
        Clinic,
        verbose_name=_("Clínica"),
        on_delete=models.PROTECT,
        related_name="documents"
    )

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("Tipo do Objeto Pai"),
        on_delete=models.CASCADE
    )
    object_id = models.UUIDField(
        verbose_name=_("ID do Objeto Pai")
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    type = models.CharField(
        verbose_name=_("Tipo do Documento"),
        max_length=16,
        choices=AllDocumentTypes
    )
    file = models.FileField(
        verbose_name=_("Arquivo"),
        storage=get_document_storage,
        upload_to='raw/%Y/%m/%d/'
    )
    sha256 = models.CharField(
        verbose_name=_("Hash SHA-256"),
        max_length=64,
        editable=False,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Enviado por"),
        on_delete=models.PROTECT,
        related_name="uploaded_documents"
    )
    created_at = models.DateTimeField(
        verbose_name=_("Data de Envio"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("Documento")
        verbose_name_plural = _("Documentos")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"{self.get_type_display()} de {self.content_object}" # type: ignore

    def _calculate_hash(self):
        hasher = hashlib.sha256()
        self.file.seek(0)
        for chunk in self.file.chunks():
            hasher.update(chunk)
        self.file.seek(0)
        return hasher.hexdigest()

    def save(self, *args, **kwargs):
        if self.content_object and hasattr(self.content_object, 'clinic'):
            self.clinic = self.content_object.clinic

        if not self.pk:
            self.sha256 = self._calculate_hash()

        super().save(*args, **kwargs)