import hashlib
import uuid
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from organization.models import Clinic
from billing.models import Guide
from .storages import DocumentStorage

from django.utils.text import slugify
from datetime import datetime

def document_upload_to(instance, filename):
    clinic_name = slugify(instance.clinic.name)
    parent_folder = slugify(instance.content_object._meta.verbose_name_plural)
    
    # Safely get parent name
    if hasattr(instance.content_object, 'full_name'):
        parent_name = slugify(instance.content_object.full_name)
    else:
        parent_name = slugify(str(instance.content_object))

    doc_type_slug = slugify(instance.type.name)
    date_path = datetime.now().strftime('%Y/%m/%d')

    return f'{clinic_name}/{parent_folder}/{parent_name}/{doc_type_slug}/{date_path}/{filename}'

class DocumentType(models.Model):
    class Category(models.TextChoices):
        PATIENT = 'PATIENT', _('Documento do Paciente')
        GUIDE = 'GUIDE', _('Documento de Guia')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        _("Nome do Tipo de Documento"),
        max_length=100,
        unique=True
    )
    category = models.CharField(
        _("Categoria"),
        max_length=10,
        choices=Category.choices
    )
    is_active = models.BooleanField(_("Ativo"), default=True)

    class Meta:
        verbose_name = _("Tipo de Documento")
        verbose_name_plural = _("Tipos de Documentos")
        ordering = ['name']

    def __str__(self):
        return self.name

document_storage = DocumentStorage()

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
    type = models.ForeignKey(
        DocumentType,
        verbose_name=_("Tipo do Documento"),
        on_delete=models.PROTECT
    )
    description = models.CharField(
        _("Descrição"),
        max_length=255,
        blank=True,
        help_text=_("Descrição customizada para o documento, usada para documentos opcionais/outros.")
    )
    file = models.FileField(
        verbose_name=_("Arquivo"),
        upload_to=document_upload_to,
        storage=document_storage
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
        return f"{self.type.name} de {self.content_object}"

    def _calculate_hash(self):
        hasher = hashlib.sha256()
        self.file.seek(0)
        for chunk in self.file.chunks():
            hasher.update(chunk)
        self.file.seek(0)
        return hasher.hexdigest()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.sha256 = self._calculate_hash()

        super().save(*args, **kwargs)