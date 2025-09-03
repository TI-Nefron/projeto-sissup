from django.db import models
from django.utils.translation import gettext_lazy as _
from documents.constants import DocumentType
from billing.models import Payer, Guide

class ParameterRule(models.Model):
    """
    Define a regra de obrigatoriedade de um documento para uma combinação
    de Pagador, Tipo de Guia e Natureza.
    """
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE)
    guide_type = models.CharField(_("Tipo de Guia"), max_length=16, choices=Guide.GuideType.choices)
    nature = models.CharField(_("Natureza"), max_length=10, choices=Guide.Nature.choices)
    document_type = models.CharField(_("Tipo de Documento"), max_length=16, choices=AllDocumentTypes)
    is_mandatory = models.BooleanField(_("Obrigatório"), default=True)

    class Meta:
        verbose_name = _("Regra de Parâmetro")
        verbose_name_plural = _("Regras de Parâmetros")
        unique_together = ('payer', 'guide_type', 'nature', 'document_type')

    def __str__(self):
        return f"{self.payer}: Exigir {self.get_document_type_display()} para {self.get_guide_type_display()} ({self.get_nature_display()})"