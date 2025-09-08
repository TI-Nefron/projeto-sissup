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
              v-model="patient.clinic"
              :items="clinics"
              item-title="name"
              item-value="id"
              label="Clínica"
              required
            ></v-select>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <v-select
              v-model="patient.patient_type"
              :items="patientTypes"
              label="Tipo"
              required
            ></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="patient.status"
              :items="patientStatuses"
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
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '@/services/api';

const route = useRoute();
const router = useRouter();

const patient = ref({
  full_name: '',
  cpf: '',
  cns: '',
  clinic: null,
  patient_type: 'CHRONIC',
  status: 'IN_TREATMENT',
});

const clinics = ref([]);
const patientTypes = ref(['CHRONIC', 'ACUTE']);
const patientStatuses = ref(['IN_TREATMENT', 'DISCHARGED', 'DECEASED', 'TRANSFERRED']);

const formTitle = computed(() => {
  return route.params.id ? 'Editar Paciente' : 'Novo Paciente';
});

onMounted(async () => {
  // Carregar clínicas
  try {
    const response = await apiClient.get('/api/clinics/');
    clinics.value = response.data;
  } catch (error) {
    console.error('Error fetching clinics:', error);
  }

  // Se for edição, carregar dados do paciente
  if (route.params.id) {
    try {
      const response = await apiClient.get(`/api/pacientes/${route.params.id}/`);
      patient.value = response.data;
    } catch (error) {
      console.error('Error fetching patient:', error);
    }
  }
});

const savePatient = async () => {
  try {
    if (route.params.id) {
      // Atualizar
      await apiClient.put(`/api/pacientes/${route.params.id}/`, patient.value);
    } else {
      // Criar
      await apiClient.post('/api/pacientes/', patient.value);
    }
    router.push('/patients');
  } catch (error) {
    console.error('Error saving patient:', error);
    // Aqui você pode adicionar um feedback para o usuário, como um snackbar de erro
  }
};
</script>
