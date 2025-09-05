
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from billing.models import Guide

class GuideType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        _("Nome do Tipo de Guia"),
        max_length=100,
        unique=True
    )
    is_active = models.BooleanField(_("Ativo"), default=True)

    class Meta:
        verbose_name = _("Tipo de Guia")
        verbose_name_plural = _("Tipos de Guias")
        ordering = ['name']

    def __str__(self):
        return self.name

class ProcedureStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        _("Nome do Status"),
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        _("Identificador (slug)"),
        max_length=100,
        unique=True,
        help_text=_("Identificador único para uso interno no código (ex: DRAFT, APPROVED). Não altere após a criação.")
    )
    is_active = models.BooleanField(_("Ativo"), default=True)

    class Meta:
        verbose_name = _("Status de Procedimento")
        verbose_name_plural = _("Status de Procedimentos")
        ordering = ['name']

    def __str__(self):
        return self.name

class ParameterRule(models.Model):
    class Context(models.TextChoices):
        PATIENT_REGISTRATION = 'PATIENT', _('Cadastro de Paciente')
        GUIDE = 'GUIDE', _('Guia de Faturamento')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    payer = models.ForeignKey(
        'billing.Payer',
        verbose_name=_("Convênio"),
        on_delete=models.CASCADE,
        related_name="parameter_rules"
    )
    context = models.CharField(
        verbose_name=_("Contexto"),
        max_length=10,
        choices=Context.choices,
        default=Context.GUIDE
    )
    guide_type = models.ForeignKey(
        GuideType,
        verbose_name=_("Tipo de Guia"),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    nature = models.CharField(
        verbose_name=_("Natureza"),
        max_length=10,
        choices=Guide.Nature.choices,
        blank=True
    )
    required_documents = models.ManyToManyField(
        'documents.DocumentType',
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
        payer_name = self.payer.name if hasattr(self, 'payer') else 'N/A'
        
        if self.context == self.Context.PATIENT_REGISTRATION:
            return f"Regra de Paciente para {payer_name}"
        
        guide_type_str = self.guide_type.name if self.guide_type else "Todos os Tipos"
        nature_str = self.get_nature_display() if self.nature else "Todas as Naturezas"
        
        return f"Regra de Guia para {payer_name} ({guide_type_str} - {nature_str})" # type: ignore