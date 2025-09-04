import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from documents.models import DocumentType
from billing.models import Payer, Guide

class ParameterRule(models.Model):
    class Context(models.TextChoices):
        PATIENT_REGISTRATION = 'PATIENT', _('Cadastro de Paciente')
        GUIDE = 'GUIDE', _('Guia de Faturamento')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    payer = models.ForeignKey(
        Payer,
        verbose_name=_("Pagador"),
        on_delete=models.CASCADE,
        related_name="parameter_rules"
    )
    context = models.CharField(
        verbose_name=_("Contexto"),
        max_length=10,
        choices=Context.choices,
        default=Context.GUIDE
    )
    guide_type = models.CharField(
        verbose_name=_("Tipo de Guia"),
        max_length=16,
        choices=Guide.GuideType.choices,
        blank=True
    )
    nature = models.CharField(
        verbose_name=_("Natureza"),
        max_length=10,
        choices=Guide.Nature.choices,
        blank=True
    )
    required_documents = models.ManyToManyField(
        DocumentType,
        verbose_name=_("Tipos de Documentos Exigidos"),
    )
    is_active = models.BooleanField(
        verbose_name=_("Regra Ativa"),
        default=True
    )

    class Meta:
        verbose_name = _("Regra de Parâmetro")
        verbose_name_plural = _("Regras de Parâmetros")
        ordering = ['payer', 'context', 'guide_type']
        
    def __str__(self):
        if self.context == self.Context.PATIENT_REGISTRATION:
            return f"Regra de Paciente para {self.payer}"
        return f"Regra de Guia para {self.payer} ({self.get_guide_type_display()} - {self.get_nature_display()})" # type: ignore