from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PatientHistory, Patient

@receiver(post_save, sender=PatientHistory)
def update_patient_status(sender, instance, created, **kwargs):
    if created:
        patient = instance.patient
        if instance.record_type == PatientHistory.RecordType.SAIDA:
            if instance.exit_type:
                patient.status = instance.exit_type.code
                patient.save()
        elif instance.record_type == PatientHistory.RecordType.ENTRADA:
            patient.status = Patient.PatientStatus.IN_TREATMENT
            patient.clinic = instance.clinic
            patient.save()