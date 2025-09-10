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
        <v-btn icon @click="showDocuments(item)" variant="text" size="small">
            <v-icon size="small">mdi-file-document-outline</v-icon>
        </v-btn>
      </template>
    </v-data-table>

    <!-- Document List Dialog -->
    <v-dialog v-model="documentDialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Documentos de {{ selectedPatient?.full_name }}</span>
        </v-card-title>
        <v-card-text>
          <v-list v-if="selectedPatientDocuments.length > 0">
            <v-list-item
              v-for="doc in selectedPatientDocuments"
              :key="doc.id"
            >
              <v-list-item-title>
                {{ doc.type.name.startsWith('Outro') ? doc.description : doc.type.name }}
              </v-list-item-title>
              <v-list-item-subtitle>
                <span v-if="doc.type.name.startsWith('Outro')">({{ doc.type.name }}) - </span>
                {{ new Date(doc.created_at).toLocaleDateString() }}
              </v-list-item-subtitle>
              <template v-slot:append>
                <v-btn icon @click="openPreview(doc)" variant="text" size="small">
                  <v-icon>mdi-eye-outline</v-icon>
                </v-btn>
                <v-btn icon :href="doc.file_url.replace('http://minio:9000', 'http://localhost:9090')" target="_blank" variant="text" size="small">
                  <v-icon>mdi-download-outline</v-icon>
                </v-btn>
              </template>
            </v-list-item>
          </v-list>
          <v-alert v-else type="info" text="Nenhum documento encontrado para este paciente."></v-alert>

          <v-divider class="my-4"></v-divider>

          <h3 class="text-h6 mb-2">Novo Documento</h3>
          <DocumentUpload
            v-if="selectedPatient"
            :content_type_str="'dialysis.patient'"
            :object_id="selectedPatient.id"
            :clinic_id="selectedPatient.clinic.id"
            @upload-completed="onUploadCompleted"
          />

        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" text @click="documentDialog = false">Fechar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Document Preview Dialog -->
    <v-dialog v-model="previewDialog" fullscreen>
        <v-card>
            <v-toolbar dark color="primary">
                <v-btn icon dark @click="previewDialog = false">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-toolbar-title>{{ selectedDocForPreview?.type.name }}</v-toolbar-title>
            </v-toolbar>
            <v-card-text class="pa-0" style="height: calc(100vh - 64px);">
                <embed v-if="selectedDocForPreview" :src="selectedDocForPreview.file_url.replace('http://minio:9000', 'http://localhost:9090')" type="application/pdf" width="100%" height="100%" />
            </v-card-text>
        </v-card>
    </v-dialog>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import apiClient from '@/services/api';
import DocumentUpload from '@/components/DocumentUpload.vue';
import { useClinicStore } from '@/stores/clinic';

// Interfaces
interface DocumentType { id: string; name: string; }
interface Document { id: string; type: DocumentType; description?: string; file_url: string; created_at: string; }
interface Clinic { id: string; name: string; }
interface Patient { id: string; full_name: string; cpf: string; cns: string; clinic: Clinic; status: string; patient_type: string; documents: Document[]; }

const clinicStore = useClinicStore();

const patients = ref<Patient[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

// Document Dialogs State
const documentDialog = ref(false);
const selectedPatient = ref<Patient | null>(null);
const selectedPatientDocuments = ref<Document[]>([]);
const previewDialog = ref(false);
const selectedDocForPreview = ref<Document | null>(null);

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

const showDocuments = (patient: Patient) => {
  selectedPatient.value = patient;
  selectedPatientDocuments.value = patient.documents || [];
  documentDialog.value = true;
};

const openPreview = (doc: Document) => {
    selectedDocForPreview.value = doc;
    previewDialog.value = true;
}

const onUploadCompleted = async () => {
  const currentPatient = selectedPatient.value;
  if (currentPatient) {
    try {
      const response = await apiClient.get<Patient>(`/api/pacientes/${currentPatient.id}/`);
      const index = patients.value.findIndex(p => p.id === currentPatient.id);
      if (index !== -1) {
        patients.value[index] = response.data;
      }
      selectedPatientDocuments.value = response.data.documents || [];
    } catch (error) {
      console.error('Erro ao recarregar dados do paciente:', error);
    }
  }
};

</script>
