import uuid
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

class Payer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        verbose_name=_("Nome do Pagador"),
        max_length=100,
        unique=True
    )
    is_active = models.BooleanField(
        verbose_name=_("Ativo"),
        default=True
    )

    class Meta:
        verbose_name = _("Pagador")
        verbose_name_plural = _("Pagadores")
        ordering = ['name']

    def __str__(self):
        return self.name

class Guide(models.Model):
    class GuideType(models.TextChoices):
        APAC = 'APAC', _('APAC')
        SADT = 'SADT', _('Guia SADT')
        CONSULTA = 'CONSULTA', _('Consulta')
        INTERNACAO = 'INTERNACAO', _('Internação')

    class Nature(models.TextChoices):
        CHRONIC = 'CHRONIC', _('Crônico')
        ACUTE = 'ACUTE', _('Agudo')

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Rascunho')
        IN_REVIEW = 'IN_REVIEW', _('Em Auditoria')
        APPROVED = 'APPROVED', _('Aprovada')
        BILLED = 'BILLED', _('Faturada')
        DENIED = 'DENIED', _('Glosada')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    patient = models.ForeignKey(
        'dialysis.Patient',
        verbose_name=_("Paciente"),
        on_delete=models.PROTECT,
        related_name="guides"
    )
    payer = models.ForeignKey(
        Payer,
        verbose_name=_("Pagador (Convênio)"),
        on_delete=models.PROTECT,
        related_name="guides",
        null=True,
        blank=True
    )
    
    guide_type = models.CharField(
        verbose_name=_("Tipo de Guia"),
        max_length=16,
        choices=GuideType.choices
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
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=16,
        choices=Status.choices,
        default=Status.DRAFT
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
        return f"{self.get_guide_type_display()} de {self.patient.full_name} ({self.created_at.strftime('%d/%m/%Y')})" # type: ignore