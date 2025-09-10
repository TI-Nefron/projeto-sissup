<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4">Dashboard</h1>
        <p class="text-subtitle-1">Resumo do sistema</p>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <!-- Patients Card -->
      <v-col cols="12" md="4">
        <v-card class="mx-auto" elevation="2" @click="$router.push('/patients')">
          <v-card-item>
            <template v-slot:prepend>
              <v-icon size="40" color="primary">mdi-account-group-outline</v-icon>
            </template>
            <v-card-title class="text-h5">{{ patientCount }}</v-card-title>
            <v-card-subtitle>Pacientes Ativos</v-card-subtitle>
          </v-card-item>
        </v-card>
      </v-col>

      <!-- Guides Card -->
      <v-col cols="12" md="4">
        <v-card class="mx-auto" elevation="2" @click="$router.push('/guides')">
          <v-card-item>
            <template v-slot:prepend>
              <v-icon size="40" color="secondary">mdi-file-document-multiple-outline</v-icon>
            </template>
            <v-card-title class="text-h5">{{ guideCount }}</v-card-title>
            <v-card-subtitle>Guias Totais</v-card-subtitle>
          </v-card-item>
        </v-card>
      </v-col>

      <!-- Add more cards as needed -->

    </v-row>

    <v-row class="mt-8">
      <v-col cols="12">
        <h2 class="text-h5">Acesso Rápido</h2>
      </v-col>
      <v-col cols="12" md="4" sm="6">
        <v-card
          class="text-center pa-4" 
          hover 
          to="/patients/new"
        >
          <v-icon size="48" color="primary">mdi-account-plus-outline</v-icon>
          <v-card-title>Novo Paciente</v-card-title>
        </v-card>
      </v-col>
      <v-col cols="12" md="4" sm="6">
        <v-card
          class="text-center pa-4" 
          hover 
          to="/guides/new"
        >
          <v-icon size="48" color="secondary">mdi-file-plus-outline</v-icon>
          <v-card-title>Nova Guia</v-card-title>
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import apiClient from '@/services/api';

const patientCount = ref(0);
const guideCount = ref(0);

const fetchData = async () => {
  try {
    // Fetch only active patients
    const patientResponse = await apiClient.get('/api/pacientes/', { params: { is_active: true } });
    patientCount.value = patientResponse.data.length;

    // Fetch all guides
    const guideResponse = await apiClient.get('/api/guias/');
    guideCount.value = guideResponse.data.length;

  } catch (error) {
    console.error('Error fetching dashboard data:', error);
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.v-card {
  transition: all 0.2s ease-in-out;
}
.v-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
}
</style>
