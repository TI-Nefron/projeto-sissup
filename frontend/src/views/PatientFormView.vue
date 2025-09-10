<template>
  <div>
    <h1 class="text-h5 my-4">{{ formTitle }}</h1>
    <v-form @submit.prevent="savePatient">
      <v-container>
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="patient.full_name"
              label="Nome Completo"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="patient.cpf"
              label="CPF"
              required
              maxlength="14"
              :rules="[cpfRule]"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="patient.cns"
              label="CNS"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="patient.clinic_id"
              :items="clinics"
              item-title="name"
              item-value="id"
              label="Clínica"
              required
              :readonly="true"
              :disabled="true"
            ></v-select>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <v-select
              v-model="patient.patient_type"
              :items="patientTypes"
              item-title="title"
              item-value="value"
              label="Tipo"
              required
            ></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="patient.status"
              :items="patientStatuses"
              item-title="title"
              item-value="value"
              label="Status"
              required
            ></v-select>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-btn type="submit" color="primary">Salvar</v-btn>
            <v-btn to="/patients" class="ml-2">Cancelar</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '@/services/api';

const route = useRoute();
const router = useRouter();

const patient = ref({
  full_name: '',
  cpf: '',
  cns: '',
  clinic_id: null,
  patient_type: 'CHRONIC',
  status: 'IN_TREATMENT',
});

const clinics = ref([]);
const patientTypes = ref([
    { title: 'Crônico', value: 'CHRONIC' },
    { title: 'Agudo', value: 'ACUTE' }
]);
const patientStatuses = ref([
    { title: 'Em Tratamento', value: 'IN_TREATMENT' },
    { title: 'Alta Ambulatorial', value: 'DISCHARGED' },
    { title: 'Óbito', value: 'DECEASED' },
    { title: 'Transferido', value: 'TRANSFERRED' }
]);

const formTitle = computed(() => {
  return route.params.id ? 'Editar Paciente' : 'Novo Paciente';
});

const cpfRule = (v: string) => {
    if (!v) return 'Este campo é obrigatório';
    return /(\d{3}\.\d{3}\.\d{3}-\d{2})/.test(v) || 'Formato de CPF inválido (XXX.XXX.XXX-XX)';
}

watch(() => patient.value.cpf, (newValue) => {
  if (newValue) {
    const cleaned = newValue.replace(/\D/g, '');
    let formatted = cleaned;
    if (cleaned.length > 3) {
      formatted = `${cleaned.slice(0, 3)}.${cleaned.slice(3)}`;
    }
    if (cleaned.length > 6) {
      formatted = `${formatted.slice(0, 7)}.${cleaned.slice(6)}`;
    }
    if (cleaned.length > 9) {
      formatted = `${formatted.slice(0, 11)}-${cleaned.slice(9)}`;
    }
    patient.value.cpf = formatted.slice(0, 14);
  }
});


onMounted(async () => {
  try {
    const response = await apiClient.get('/api/clinics/');
    clinics.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar clínicas:', error);
  }

  if (route.params.id) {
    try {
      const response = await apiClient.get(`/api/pacientes/${route.params.id}/`);
      const patientData = response.data;
      patient.value = {
          ...patientData,
          clinic_id: patientData.clinic.id
      }
    } catch (error) {
      console.error('Erro ao buscar paciente:', error);
    }
  } else if (route.query.clinicId) {
    // Se é um novo paciente, preenche a clínica a partir da query param
    patient.value.clinic_id = route.query.clinicId as string;
  }
});

const savePatient = async () => {
  try {
    const payload = {
        ...patient.value,
        clinic: patient.value.clinic_id
    }
    if (route.params.id) {
      await apiClient.put(`/api/pacientes/${route.params.id}/`, payload);
    } else {
      await apiClient.post('/api/pacientes/', payload);
    }
    router.push('/patients');
  } catch (error) {
    console.error('Erro ao salvar paciente:', error);
  }
};
</script>