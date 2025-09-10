<template>
  <v-container>
    <h1 class="text-h5 my-4">Guias de Faturamento</h1>

    <!-- Error Alert -->
    <v-alert v-if="error" type="error" class="mb-4" closable>
      {{ error }}
    </v-alert>

    <!-- Filter section -->
    <v-expansion-panels class="mb-4">
      <v-expansion-panel>
        <v-expansion-panel-title>Filtros</v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-row>
            <v-col cols="12" md="4">
              <v-text-field v-model="filters.patient__full_name__icontains" label="Nome do Paciente" clearable></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-select v-model="filters.payer" :items="payers" item-title="name" item-value="id" label="Convênio" clearable></v-select>
            </v-col>
            <v-col cols="12" md="4">
              <v-select v-model="filters.guide_type" :items="guideTypes" item-title="name" item-value="id" label="Tipo de Guia" clearable></v-select>
            </v-col>
            <v-col cols="12" md="4">
              <v-select v-model="filters.status" :items="statuses" item-title="name" item-value="id" label="Status" clearable></v-select>
            </v-col>
            <v-col cols="12" md="4">
              <v-select v-model="filters.nature" :items="natureOptions" item-title="title" item-value="value" label="Natureza" clearable></v-select>
            </v-col>
            <v-col cols="12" md="6">
              <v-menu v-model="dateMenuFrom" :close-on-content-click="false" transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ props }">
                  <v-text-field v-model="filters.valid_from__gte" label="Vigência De" prepend-icon="mdi-calendar" readonly v-bind="props" clearable></v-text-field>
                </template>
                <v-date-picker v-model="filters.valid_from__gte" @update:model-value="dateMenuFrom = false"></v-date-picker>
              </v-menu>
            </v-col>
            <v-col cols="12" md="6">
              <v-menu v-model="dateMenuTo" :close-on-content-click="false" transition="scale-transition" offset-y min-width="auto">
                <template v-slot:activator="{ props }">
                  <v-text-field v-model="filters.valid_to__lte" label="Vigência Até" prepend-icon="mdi-calendar" readonly v-bind="props" clearable></v-text-field>
                </template>
                <v-date-picker v-model="filters.valid_to__lte" @update:model-value="dateMenuTo = false"></v-date-picker>
              </v-menu>
            </v-col>
          </v-row>
          <v-btn @click="clearFilters" class="ml-2">Limpar Filtros</v-btn>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-toolbar flat>
        <v-toolbar-title>Lista de Guias</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-btn color="primary" dark class="mb-2" :to="`/guides/new?clinicId=${clinicStore.selectedClinic?.id}`">Nova Guia</v-btn>
    </v-toolbar>

    <!-- Skeleton Loader -->
    <v-skeleton-loader v-if="loading" type="table-tbody@3"></v-skeleton-loader>

    <!-- Data Table -->
    <v-data-table
      v-else
      :headers="headers"
      :items="guides"
      class="elevation-1"
    >
      <template #[`item.status.name`]='{ value }'>
        <v-chip :color="getStatusColor(value)" :text="value" size="small"></v-chip>
      </template>
      <template #[`item.actions`]="{ item }">
        <v-btn icon :to="`/guides/${item.id}/edit`" variant="text" size="small">
            <v-icon size="small">mdi-pencil</v-icon>
        </v-btn>
        <v-btn icon @click="showDocuments(item)" variant="text" size="small">
            <v-icon size="small">mdi-file-document-outline</v-icon>
        </v-btn>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Documentos da Guia</span>
        </v-card-title>
        <v-card-text>
          <v-list v-if="selectedGuideDocuments.length > 0">
            <v-list-item
              v-for="doc in selectedGuideDocuments"
              :key="doc.id"
            >
              <template v-slot:prepend>
                <v-checkbox v-model="selectedDocuments" :value="doc"></v-checkbox>
              </template>
              <v-list-item-title>{{ doc.type.name }}</v-list-item-title>
              <v-list-item-subtitle>{{ new Date(doc.created_at).toLocaleDateString() }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
          <v-alert v-else type="info" text="Nenhum documento encontrado para esta guia."></v-alert>

          <v-divider class="my-4"></v-divider>

          <h3 class="text-h6 mb-2">Novo Documento</h3>
          <DocumentUpload
            v-if="selectedGuide"
            :content_type_str="'billing.guide'"
            :object_id="selectedGuide.id"
            :clinic_id="selectedGuide.clinic.id"
            @upload-completed="onUploadCompleted"
          />

        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">Fechar</v-btn>
          <v-btn color="primary" :disabled="selectedDocuments.length !== 2" @click="compareDocuments">Comparar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <DocumentViewer
      v-model="viewerDialog"
      :doc1url="doc1url"
      :doc2url="doc2url"
    />
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import apiClient from '@/services/api';
import DocumentViewer from '@/components/DocumentViewer.vue';
import DocumentUpload from '@/components/DocumentUpload.vue';
import { useClinicStore } from '@/stores/clinic';

// Interfaces
interface DocumentType {
  id: string;
  name: string;
}

interface Document {
  id: string;
  type: DocumentType;
  file_url: string;
  created_at: string;
}

interface Clinic {
  id: string;
  name: string;
}

interface Payer {
  id: string;
  name: string;
}

interface GuideType {
  id: string;
  name: string;
}

interface ProcedureStatus {
  id: string;
  name: string;
}

interface Patient {
    id: string;
    full_name: string;
}

interface Guide {
  id: string;
  patient: Patient;
  clinic: Clinic;
  payer: Payer;
  guide_type: GuideType;
  status: ProcedureStatus;
  authorization_number: string;
  valid_from: string;
  valid_to: string;
  documents: Document[];
}

const clinicStore = useClinicStore();

const guides = ref<Guide[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const filters = ref({
  patient__full_name__icontains: '',
  clinic: null as string | null,
  payer: null as string | null,
  guide_type: null as string | null,
  status: null as string | null,
  nature: null as string | null,
  valid_from__gte: null as string | null,
  valid_to__lte: null as string | null,
});

const dateMenuFrom = ref(false);
const dateMenuTo = ref(false);

const clinics = ref<Clinic[]>([]);
const payers = ref<Payer[]>([]);
const guideTypes = ref<GuideType[]>([]);
const statuses = ref<ProcedureStatus[]>([]);
const natureOptions = ref([
    { title: 'Crônico', value: 'CHRONIC' },
    { title: 'Agudo', value: 'ACUTE' }
]);
const dialog = ref(false);
const selectedGuide = ref<Guide | null>(null);
const selectedGuideDocuments = ref<Document[]>([]);
const selectedDocuments = ref<Document[]>([]);
const viewerDialog = ref(false);
const doc1url = ref('');
const doc2url = ref('');

let debounceTimer: number;

const headers = ref([
  { title: 'Paciente', value: 'patient.full_name' },
  { title: 'Convênio', value: 'payer.name' },
  { title: 'Tipo Guia', value: 'guide_type.name' },
  { title: 'Status', value: 'status.name' },
  { title: 'Nº Autorização', value: 'authorization_number' },
  { title: 'Vigência Início', value: 'valid_from' },
  { title: 'Vigência Fim', value: 'valid_to' },
  { title: 'Ações', key: 'actions', sortable: false },
]);

const fetchGuides = async () => {
  if (!clinicStore.selectedClinic) {
    error.value = 'Nenhuma clínica selecionada.';
    return;
  }
  loading.value = true;
  error.value = null;
  try {
    const activeFilters = Object.fromEntries(
      Object.entries(filters.value).filter(([, value]) => value !== null && value !== '')
    );
    
    // Adiciona a clínica selecionada como um filtro fixo
    const params = { ...activeFilters, clinic: clinicStore.selectedClinic.id };

    const response = await apiClient.get<Guide[]>('/api/guias/', { params });
    guides.value = response.data;
  } catch (err) {
    console.error('Erro ao buscar guias:', err);
    error.value = 'Falha ao carregar as guias. Tente novamente mais tarde.';
  } finally {
    loading.value = false;
  }
};

const fetchFilterOptions = async () => {
  if (!clinicStore.selectedClinic) return;
  try {
    const clinicId = clinicStore.selectedClinic.id;
    const [payerRes, guideTypeRes, statusRes] = await Promise.all([
      apiClient.get<Payer[]>(`/api/clinics/${clinicId}/payers/`),
      apiClient.get<GuideType[]>(`/api/clinics/${clinicId}/guide-types/`),
      apiClient.get<ProcedureStatus[]>(`/api/clinics/${clinicId}/procedure-statuses/`),
    ]);
    payers.value = payerRes.data;
    guideTypes.value = guideTypeRes.data;
    statuses.value = statusRes.data;
  } catch (error) {
    console.error('Erro ao buscar opções de filtro:', error);
  }
};

const getStatusColor = (status: string) => {
  const lowerCaseStatus = status.toLowerCase();
  if (lowerCaseStatus.includes('autorizado')) return 'green';
  if (lowerCaseStatus.includes('pendente')) return 'orange';
  if (lowerCaseStatus.includes('negado')) return 'red';
  if (lowerCaseStatus.includes('cancelado')) return 'grey';
  return 'primary'; // Default color
};

watch(filters, () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetchGuides();
  }, 500); // 500ms debounce
}, { deep: true });

const clearFilters = () => {
  filters.value = {
    patient__full_name__icontains: '',
    clinic: null,
    payer: null,
    guide_type: null,
    status: null,
    nature: null,
    valid_from__gte: null,
    valid_to__lte: null,
  };
  // The watch will trigger fetchGuides
};

const showDocuments = (guide: Guide) => {
  selectedGuide.value = guide;
  selectedGuideDocuments.value = guide.documents || [];
  selectedDocuments.value = [];
  dialog.value = true;
};

const compareDocuments = () => {
  if (selectedDocuments.value.length === 2) {
    doc1url.value = 'http://localhost:9090' + selectedDocuments.value[0].file_url;
    doc2url.value = 'http://localhost:9090' + selectedDocuments.value[1].file_url;
    viewerDialog.value = true;
  }
};

const onUploadCompleted = async () => {
  // Refetch guides to get updated document info
  await fetchGuides();
  // Find the updated guide and refresh its documents in the dialog
  const currentGuide = selectedGuide.value;
  if (currentGuide) {
    const updatedGuide = guides.value.find(g => g.id === currentGuide.id);
    if (updatedGuide) {
      selectedGuideDocuments.value = updatedGuide.documents || [];
    }
  }
};

watch(() => clinicStore.selectedClinic, (newClinic, oldClinic) => {
  if (newClinic && newClinic.id !== oldClinic?.id) {
    fetchGuides();
  }
});

onMounted(() => {
  fetchGuides();
  fetchFilterOptions();
});
</script>
