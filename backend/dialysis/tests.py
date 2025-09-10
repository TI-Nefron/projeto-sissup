from django.test import TestCase
from organization.models import Clinic
from .models import Patient

class DialysisModelsTestCase(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(name="Test Clinic", cnpj="12.345.678/0001-99")

    def test_create_patient(self):
        """Test that a Patient can be created and is active by default."""
        patient = Patient.objects.create(
            clinic=self.clinic,
            full_name="Test Patient",
            cpf="123.456.789-00",
            cns="123456789012345"
        )
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(patient.full_name, "Test Patient")
        self.assertTrue(patient.is_active)

    def test_patient_inactive_on_status_change(self):
        """Test that the is_active flag is set to False for inactive statuses."""
        patient = Patient.objects.create(
            clinic=self.clinic,
            full_name="Test Patient",
            cpf="123.456.789-00",
            cns="123456789012345"
        )
        self.assertTrue(patient.is_active)

        # Change status to an inactive one
        patient.status = Patient.PatientStatus.DECEASED
        patient.save()

        self.assertFalse(patient.is_active)

        # Change status back to an active one
        patient.status = Patient.PatientStatus.IN_TREATMENT
        patient.save()

        self.assertTrue(patient.is_active)