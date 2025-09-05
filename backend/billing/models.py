import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from organization.models import Clinic

class Payer(models.Model):
    class PayerType(models.TextChoices):
        SUS = 'SUS', _('SUS')
        PRIVATE = 'PRIVATE', _('Convênio Privado')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        _("Nome do Convênio"),
        max_length=100,
        unique=True
    )
    payer_type = models.CharField(
        _("Tipo"),
        max_length=10,
        choices=PayerType.choices,
        default=PayerType.PRIVATE
    )
    clinics = models.ManyToManyField(
        Clinic,
        verbose_name=_("Clínicas Atendidas"),
        related_name="payers",
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name=_("Ativo"),
        default=True
    )

    class Meta:
        verbose_name = _("Convênio")
        verbose_name_plural = _("Convênios")
        ordering = ['name']

    def __str__(self):
        return self.name

class Guide(models.Model):
    class Nature(models.TextChoices):
        CHRONIC = 'CHRONIC', _('Crônico')
        ACUTE = 'ACUTE', _('Agudo')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    patient = models.ForeignKey(
        'dialysis.Patient',
        verbose_name=_("Paciente"),
        on_delete=models.PROTECT,
        related_name="guides"
    )
    clinic = models.ForeignKey(
        Clinic,
        verbose_name=_("Clínica"),
        on_delete=models.PROTECT,
        related_name="guides"
    )
    payer = models.ForeignKey(
        Payer,
        verbose_name=_("Convênio"),
        on_delete=models.PROTECT,
        related_name="guides",
        null=True,
        blank=True
    )
    
    guide_type = models.ForeignKey(
        'parameters.GuideType',
        verbose_name=_("Tipo de Guia"),
        on_delete=models.PROTECT
    )
    nature = models.CharField(
        verbose_name=_("Natureza (Crônico/Agudo)"),
        max_length=10,
        choices=Nature.choices
    )
    authorization_number = models.CharField(
        verbose_name=_("Número da Autorização/Guia"),
        max_length=50,
        blank=True
    )
    status = models.ForeignKey(
        'parameters.ProcedureStatus',
        verbose_name=_("Status"),
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    
    valid_from = models.DateField(verbose_name=_("Vigência (Início)"), null=True, blank=True)
    valid_to = models.DateField(verbose_name=_("Vigência (Fim)"), null=True, blank=True)
    
    documents = GenericRelation('documents.Document')

    created_at = models.DateTimeField(verbose_name=_("Data de Criação"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Última Atualização"), auto_now=True)

    class Meta:
        verbose_name = _("Guia")
        verbose_name_plural = _("Guias")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.guide_type.name} de {self.patient.full_name} ({self.created_at.strftime('%d/%m/%Y')})"

    def save(self, *args, **kwargs):
        if self.patient:
            self.clinic = self.patient.clinic
        super().save(*args, **kwargs)