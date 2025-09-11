<template>
  <div>
    <h1 class="text-h5 my-4">Pacientes</h1>

    <!-- Error Alert -->
    <v-alert v-if="error" type="error" class="mb-4" closable>
      {{ error }}
    </v-alert>

    <v-toolbar flat>
      <v-toolbar-title>Lista de Pacientes</v-toolbar-title>
      <v-divider class="mx-4" inset vertical></v-divider>
      <v-spacer></v-spacer>
      <v-btn color="primary" dark class="mb-2" to="/patients/new">Novo Paciente</v-btn>
    </v-toolbar>

    <!-- Skeleton Loader -->
    <v-skeleton-loader v-if="loading" type="table-tbody@5"></v-skeleton-loader>

    <!-- Data Table -->
    <v-data-table
      v-else
      :headers="headers"
      :items="patients"
      class="elevation-1"
    >
      <template #[`item.cpf`]='{ value }'>
        {{ formatCPF(value) }}
      </template>
      <template #[`item.cns`]='{ value }'>
        {{ formatCNS(value) }}
      </template>
      <template #[`item.status`]='{ value }'>
        <v-chip :color="getStatusColor(value)" :text="translateStatus(value)" size="small"></v-chip>
      </template>
      <template #[`item.patient_type`]='{ value }'>
        <v-chip :color="getPatientTypeColor(value)" :text="translatePatientType(value)" size="small"></v-chip>
      </template>
      <template #[`item.actions`]="{ item }">
        <v-btn icon :to="`/patients/${item.id}/edit`" variant="text" size="small">
            <v-icon size="small">mdi-pencil</v-icon>
        </v-btn>
        <v-btn icon @click="showObjectHistory(item, 'dialysis', 'patient')" variant="text" size="small">
            <v-icon size="small">mdi-history</v-icon>
        </v-btn>
      </template>
    </v-data-table>

    <ObjectHistory 
      v-if="historyTarget"
      v-model="historyDialog"
      :object-id="historyTarget.id"
      :content-type-app-label="historyTarget.appLabel"
      :content-type-model="historyTarget.model"
    />

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import apiClient from '@/services/api';
import ObjectHistory from '@/components/ObjectHistory.vue';
import { useClinicStore } from '@/stores/clinic';

// Interfaces
interface Clinic { id: string; name: string; }
interface Patient { id: string; full_name: string; cpf: string; cns: string; clinic: Clinic; status: string; patient_type: string; }

const clinicStore = useClinicStore();

const patients = ref<Patient[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

// Dialogs State
const historyDialog = ref(false);
const historyTarget = ref<{ id: string; appLabel: string; model: string; } | null>(null);

const headers = ref([
  { title: 'Nome Completo', value: 'full_name' },
  { title: 'CPF', value: 'cpf' },
  { title: 'CNS', value: 'cns' },
  { title: 'Clínica', value: 'clinic.name' },
  { title: 'Status', value: 'status' },
  { title: 'Tipo', value: 'patient_type' },
  { title: 'Ações', key: 'actions', sortable: false },
]);

const fetchPatients = async () => {
  if (!clinicStore.selectedClinic) {
    error.value = 'Nenhuma clínica selecionada.';
    return;
  }
  loading.value = true;
  try {
    const response = await apiClient.get<Patient[]>('/api/pacientes/', { params: { clinic: clinicStore.selectedClinic.id } });
    patients.value = response.data;
  } catch (err) {
    console.error('Erro ao buscar pacientes:', err);
    error.value = 'Falha ao carregar os pacientes. Tente novamente mais tarde.';
  } finally {
    loading.value = false;
  }
};

function showObjectHistory(item: { id: string }, appLabel: string, model: string) {
  historyTarget.value = { id: item.id, appLabel, model };
  historyDialog.value = true;
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'IN_TREATMENT': return 'blue';
    case 'DISCHARGED': return 'green';
    case 'DECEASED': return 'red';
    case 'TRANSFERRED': return 'orange';
    default: return 'grey';
  }
};

const getPatientTypeColor = (type: string) => {
  return type === 'CHRONIC' ? 'purple' : 'teal';
};

const translateStatus = (status: string) => {
  const translations: { [key: string]: string } = {
    IN_TREATMENT: 'Em Tratamento',
    DISCHARGED: 'Alta',
    DECEASED: 'Óbito',
    TRANSFERRED: 'Transferido',
  };
  return translations[status] || status;
};

const translatePatientType = (type: string) => {
  const translations: { [key: string]: string } = {
    CHRONIC: 'Crônico',
    ACUTE: 'Agudo',
  };
  return translations[type] || type;
};

const formatCPF = (cpf: string) => {
  if (!cpf) return '';
  const cleaned = cpf.replace(/\D/g, '');
  return cleaned.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
};

const formatCNS = (cns: string) => {
  if (!cns) return '';
  const cleaned = cns.replace(/\D/g, '');
  return cleaned.replace(/(\d{3})(\d{3})(\d{3})(\d{3})(\d{3})/, '$1.$2.$3.$4.$5');
};

onMounted(fetchPatients);

watch(() => clinicStore.selectedClinic, (newClinic, oldClinic) => {
  if (newClinic && newClinic.id !== oldClinic?.id) {
    fetchPatients();
  }
});

</script>
