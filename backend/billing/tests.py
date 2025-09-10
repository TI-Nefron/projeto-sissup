from django.test import TestCase
from organization.models import Clinic
from dialysis.models import Patient
from parameters.models import GuideType
from .models import Payer, Guide

class BillingModelsTestCase(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(name="Test Clinic", cnpj="12.345.678/0001-99")
        self.patient = Patient.objects.create(
            clinic=self.clinic,
            full_name="Test Patient",
            cpf="123.456.789-00",
            cns="123456789012345"
        )
        self.guide_type = GuideType.objects.create(name="Test Guide Type")

    def test_create_payer(self):
        """Test that a Payer can be created."""
        payer = Payer.objects.create(name="Test Payer")
        self.assertEqual(Payer.objects.count(), 1)
        self.assertEqual(payer.name, "Test Payer")

    def test_create_guide(self):
        """Test that a Guide can be created."""
        payer = Payer.objects.create(name="Test Payer")
        guide = Guide.objects.create(
            patient=self.patient,
            payer=payer,
            guide_type=self.guide_type,
            nature=Guide.Nature.CHRONIC
        )
        self.assertEqual(Guide.objects.count(), 1)
        self.assertEqual(guide.patient.full_name, "Test Patient")
        self.assertEqual(guide.clinic.name, "Test Clinic") # Check auto-assignment of clinic