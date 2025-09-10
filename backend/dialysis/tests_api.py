from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from organization.models import Clinic
from .models import Patient

User = get_user_model()

class PatientAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.clinic = Clinic.objects.create(name="API Test Clinic", cnpj="98.765.432/0001-11")
        self.patient = Patient.objects.create(
            clinic=self.clinic,
            full_name="API Test Patient",
            cpf="987.654.321-00",
            cns="987654321098765"
        )
        self.client.login(username='testuser', password='testpass')
        self.user.clinics.add(self.clinic)

    def test_list_patients(self):
        """Ensure we can list patients."""
        url = '/api/pacientes/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['full_name'], 'API Test Patient')

    def test_create_patient(self):
        """Ensure we can create a new patient."""
        url = '/api/pacientes/'
        data = {
            'clinic_id': self.clinic.id,
            'full_name': 'New API Patient',
            'cpf': '111.222.333-44',
            'cns': '111222333444555'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 2)
        self.assertEqual(response.data['full_name'], 'New API Patient')
