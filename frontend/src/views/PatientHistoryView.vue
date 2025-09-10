<template>
  <v-container>
    <v-toolbar flat>
      <v-toolbar-title>Histórico de Pacientes</v-toolbar-title>
      <v-divider class="mx-4" inset vertical></v-divider>
      <v-spacer></v-spacer>
      <v-btn color="primary" dark @click="openForm">Novo Registro</v-btn>
    </v-toolbar>

    <v-data-table
      :headers="headers"
      :items="historyRecords"
      :loading="loading"
      class="elevation-1 mt-4"
    >
      <template #[`item.record_type`]='{ value }'>
        {{ translateRecordType(value) }}
      </template>
    </v-data-table>

    <PatientHistoryForm v-model="dialog" @save="onSave" />

  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import apiClient from '@/services/api';
import PatientHistoryForm from '@/components/PatientHistoryForm.vue';
import { useClinicStore } from '@/stores/clinic';

interface PatientHistory {
  id: string;
  patient: { full_name: string };
  record_type: string;
  record_date: string;
  clinic: { name: string };
  exit_type: { name: string } | null;
  notes: string;
}

const clinicStore = useClinicStore();

const historyRecords = ref<PatientHistory[]>([]);
const loading = ref(true);
const dialog = ref(false);

const headers = ref([
  { title: 'Paciente', value: 'patient.full_name' },
  { title: 'Tipo', value: 'record_type' },
  { title: 'Data', value: 'record_date' },
  { title: 'Clínica', value: 'clinic.name' },
  { title: 'Tipo de Saída', value: 'exit_type.name' },
  { title: 'Notas', value: 'notes' },
]);

const fetchHistory = async () => {
  if (!clinicStore.selectedClinic) return;
  loading.value = true;
  try {
    const response = await apiClient.get('/api/historico/', {
      params: { clinic: clinicStore.selectedClinic.id }
    });
    historyRecords.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar histórico:', error);
  } finally {
    loading.value = false;
  }
};

watch(() => clinicStore.selectedClinic, (newClinic, oldClinic) => {
  if (newClinic && newClinic.id !== oldClinic?.id) {
    fetchHistory();
  }
});

onMounted(fetchHistory);

const openForm = () => {
  dialog.value = true;
};

const onSave = () => {
  dialog.value = false;
  fetchHistory(); // Refresh list after save
};

const translateRecordType = (type: string) => {
  const translations: { [key: string]: string } = {
    ENTRADA: 'Entrada',
    SAIDA: 'Saída',
  };
  return translations[type] || type;
};

</script>
