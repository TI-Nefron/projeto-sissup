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
        <v-btn icon @click="showObjectHistory(item, 'billing', 'guide')" variant="text" size="small">
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

  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import apiClient from '@/services/api';
import ObjectHistory from '@/components/ObjectHistory.vue';
import { useClinicStore } from '@/stores/clinic';

// Interfaces
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

const payers = ref<Payer[]>([]);
const guideTypes = ref<GuideType[]>([]);
const statuses = ref<ProcedureStatus[]>([]);
const natureOptions = ref([
    { title: 'Crônico', value: 'CHRONIC' },
    { title: 'Agudo', value: 'ACUTE' }
]);

const historyDialog = ref(false);
const historyTarget = ref<{ id: string; appLabel: string; model: string; } | null>(null);

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
    
    const params = { ...activeFilters, clinic: clinicStore.selectedClinic.id };

    const response = await apiClient.get<Guide[]>('/api/billing/guides/', { params });
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
      apiClient.get<Payer[]>(`/api/billing/clinics/${clinicId}/payers/`),
      apiClient.get<GuideType[]>(`/api/parameters/clinics/${clinicId}/guide-types/`),
      apiClient.get<ProcedureStatus[]>(`/api/parameters/clinics/${clinicId}/procedure-statuses/`),
    ]);
    payers.value = payerRes.data;
    guideTypes.value = guideTypeRes.data;
    statuses.value = statusRes.data;
  } catch (error) {
    console.error('Erro ao buscar opções de filtro:', error);
  }
};

function showObjectHistory(item: { id: string }, appLabel: string, model: string) {
  historyTarget.value = { id: item.id, appLabel, model };
  historyDialog.value = true;
}

const getStatusColor = (status: string) => {
  const lowerCaseStatus = status.toLowerCase();
  if (lowerCaseStatus.includes('autorizado')) return 'green';
  if (lowerCaseStatus.includes('pendente')) return 'orange';
  if (lowerCaseStatus.includes('negado')) return 'red';
  if (lowerCaseStatus.includes('cancelado')) return 'grey';
  return 'primary'; // Default color
};

watch(() => filters.value.patient__full_name__icontains, (newValue, oldValue) => {
  if (newValue) {
    let formatted = newValue.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    formatted = formatted.replace(/\s{2,}/g, ' ');
    formatted = formatted.split(' ').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ');

    if (formatted !== newValue) {
      filters.value.patient__full_name__icontains = formatted;
    }
  }
});

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
