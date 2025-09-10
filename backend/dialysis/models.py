import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from organization.models import Clinic
from django.contrib.contenttypes.fields import GenericRelation

class ExitType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    clinics = models.ManyToManyField(
        Clinic,
        verbose_name=_("Clínicas"),
        related_name="exit_types",
        blank=True
    )

    def __str__(self):
        return self.name

class Patient(models.Model):
    """
    Represents a patient undergoing renal therapy, associated with a specific clinic
    and lifecycle status.
    """
    class PatientType(models.TextChoices):
        CHRONIC = 'CHRONIC', _('Crônico')
        ACUTE = 'ACUTE', _('Agudo')

    class PatientStatus(models.TextChoices):
        IN_TREATMENT = 'IN_TREATMENT', _('Em Tratamento')
        DISCHARGED = 'DISCHARGED', _('Alta Ambulatorial')
        DECEASED = 'DECEASED', _('Óbito')
        TRANSFERRED = 'TRANSFERRED', _('Transferido')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    clinic = models.ForeignKey(
        Clinic,
        verbose_name=_("Clínica"),
        on_delete=models.PROTECT,
        related_name="pacientes"
    )
    full_name = models.CharField(
        verbose_name=_("Nome Completo"),
        max_length=255
    )
    cpf = models.CharField(
        verbose_name=_("CPF"),
        max_length=14,
        unique=True,
        help_text=_("Formato: 123.456.789-00")
    )
    cns = models.CharField(
        verbose_name=_("Cartão Nacional de Saúde (CNS)"),
        max_length=18,
        unique=True
    )
    cid_principal = models.CharField(
        verbose_name=_("CID Principal"),
        max_length=10,
        blank=True,
        help_text=_("Código da Classificação Internacional de Doenças")
    )
    payer = models.ForeignKey(
        'billing.Payer',  # Using string reference to prevent circular import
        verbose_name=_("Pagador (Convênio)"),
        on_delete=models.PROTECT,
        related_name="pacientes",
        null=True,
        blank=True
    )
    patient_type = models.CharField(
        verbose_name=_("Tipo (Crônico/Agudo)"),
        max_length=10,
        choices=PatientType.choices,
        default=PatientType.CHRONIC
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=16,
        choices=PatientStatus.choices,
        default=PatientStatus.IN_TREATMENT
    )
    is_active = models.BooleanField(
        verbose_name=_("Cadastro Ativo"),
        default=True,
        help_text=_("Indica se o paciente está ativo no sistema. É desmarcado automaticamente para status de alta, óbito ou transferência.")
    )

    created_at = models.DateTimeField(verbose_name=_("Data de Criação"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Última Atualização"), auto_now=True)
    documents = GenericRelation('documents.Document')
    
    class Meta:
        verbose_name = _("Paciente")
        verbose_name_plural = _("Pacientes")
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically update the is_active flag
        based on the patient's status.
        """
        inactive_statuses = [
            self.PatientStatus.DISCHARGED,
            self.PatientStatus.DECEASED,
            self.PatientStatus.TRANSFERRED
        ]
        
        if self.status in inactive_statuses:
            self.is_active = False
        else:
            self.is_active = True
            
        super().save(*args, **kwargs)

class PatientHistory(models.Model):
    class RecordType(models.TextChoices):
        ENTRADA = 'ENTRADA', _('Entrada')
        SAIDA = 'SAIDA', _('Saída')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='history_records')
    record_type = models.CharField(max_length=10, choices=RecordType.choices)
    record_date = models.DateField()
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT)
    exit_type = models.ForeignKey(ExitType, on_delete=models.PROTECT, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Histórico do Paciente")
        verbose_name_plural = _("Históricos dos Pacientes")
        ordering = ['-record_date', '-created_at']

    def __str__(self):
        return f"{self.get_record_type_display()} de {self.patient.full_name} em {self.record_date}"