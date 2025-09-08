<template>
  <div>
    <h1 class="text-h5 my-4">Guias de Faturamento</h1>
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
              <v-select v-model="filters.clinic" :items="clinics" item-title="name" item-value="id" label="Clínica" clearable></v-select>
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
              <v-select v-model="filters.nature" :items="natureOptions" label="Natureza" clearable></v-select>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="filters.valid_from__gte" label="Vigência De" type="date" clearable></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="filters.valid_to__lte" label="Vigência Até" type="date" clearable></v-text-field>
            </v-col>
          </v-row>
          <v-btn @click="applyFilters">Aplicar Filtros</v-btn>
          <v-btn @click="clearFilters" class="ml-2">Limpar Filtros</v-btn>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-data-table
      :headers="headers"
      :items="guides"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:item.actions="{ item }">
        <v-icon
          size="small"
          @click="showDocuments(item.raw)"
        >
          mdi-file-document
        </v-icon>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Documentos da Guia</span>
        </v-card-title>
        <v-card-text>
          <v-list>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import apiClient from '@/services/api';
import DocumentViewer from '@/components/DocumentViewer.vue';

const guides = ref<any[]>([]);
const loading = ref(true);
const filters = ref({
  patient__full_name__icontains: '',
  clinic: null,
  payer: null,
  guide_type: null,
  status: null,
  nature: null,
  valid_from__gte: '',
  valid_to__lte: '',
});

const clinics = ref<any[]>([]);
const payers = ref<any[]>([]);
const guideTypes = ref<any[]>([]);
const statuses = ref<any[]>([]);
const natureOptions = ref(['CHRONIC', 'ACUTE']);
const dialog = ref(false);
const selectedGuideDocuments = ref<any[]>([]);
const selectedDocuments = ref<any[]>([]);
const viewerDialog = ref(false);
const doc1url = ref('');
const doc2url = ref('');

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
  loading.value = true;
  try {
    const activeFilters = Object.fromEntries(
      Object.entries(filters.value).filter(([, value]) => value !== null && value !== '')
    );
    const response = await apiClient.get('/guias/', { params: activeFilters });
    guides.value = response.data;
  } catch (error) {
    console.error('Error fetching guides:', error);
  } finally {
    loading.value = false;
  }
};

const fetchFilterOptions = async () => {
  try {
    const [clinicRes, payerRes, guideTypeRes, statusRes] = await Promise.all([
      apiClient.get('/clinics/'),
      apiClient.get('/payers/'),
      apiClient.get('/guide-types/'),
      apiClient.get('/procedure-statuses/'),
    ]);
    clinics.value = clinicRes.data;
    payers.value = payerRes.data;
    guideTypes.value = guideTypeRes.data;
    statuses.value = statusRes.data;
  } catch (error) {
    console.error('Error fetching filter options:', error);
  }
};

const applyFilters = () => {
  fetchGuides();
};

const clearFilters = () => {
  filters.value = {
    patient__full_name__icontains: '',
    clinic: null,
    payer: null,
    guide_type: null,
    status: null,
    nature: null,
    valid_from__gte: '',
    valid_to__lte: '',
  };
  fetchGuides();
};

const showDocuments = (guide: any) => {
  selectedGuideDocuments.value = guide.documents;
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

onMounted(() => {
  fetchGuides();
  fetchFilterOptions();
});
</script>
