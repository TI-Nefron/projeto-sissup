<template>
  <div>
    <h1 class="text-h5 my-4">Pacientes</h1>
    <v-data-table
      :headers="headers"
      :items="patients"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Lista de Pacientes</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-btn color="primary" dark class="mb-2">Novo Paciente</v-btn>
        </v-toolbar>
      </template>
    </v-data-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import apiClient from '@/services/api';

const patients = ref([]);
const loading = ref(true);
const headers = ref([
  { title: 'Nome Completo', value: 'full_name' },
  { title: 'CPF', value: 'cpf' },
  { title: 'CNS', value: 'cns' },
  { title: 'Clínica', value: 'clinic.name' },
  { title: 'Status', value: 'status' },
  { title: 'Tipo', value: 'patient_type' },
]);

onMounted(async () => {
  try {
    const response = await apiClient.get('/pacientes/');
    patients.value = response.data;
  } catch (error) {
    console.error('Error fetching patients:', error);
  } finally {
    loading.value = false;
  }
});
</script>
