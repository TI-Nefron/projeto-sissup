<template>
  <v-container>
    <h1 class="text-h5 my-4">{{ formTitle }}</h1>
    <v-form ref="form" @submit.prevent="saveGuide">
      <v-container>
        <v-row>
          <v-col cols="12" md="6">
            <v-autocomplete
              v-model="guide.patient"
              :items="patients"
              item-title="full_name"
              item-value="id"
              label="Paciente"
              required
              :rules="[requiredRule]"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="guide.clinic_name"
              label="Clínica"
              readonly
              disabled
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="6">
            <v-select
              v-model="guide.payer"
              :items="payers"
              item-title="name"
              item-value="id"
              label="Convênio"
              required
              :rules="[requiredRule]"
            ></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="guide.guide_type"
              :items="guideTypes"
              item-title="name"
              item-value="id"
              label="Tipo de Guia"
              required
              :rules="[requiredRule]"
            ></v-select>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="6">
            <v-select
              v-model="guide.nature"
              :items="natureOptions"
              item-title="title"
              item-value="value"
              label="Natureza"
              required
              :rules="[requiredRule]"
            ></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="guide.authorization_number"
              label="Número da Autorização"
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="4">
            <v-select
              v-model="guide.status"
              :items="statuses"
              item-title="name"
              item-value="id"
              label="Status"
              required
              :rules="[requiredRule]"
            ></v-select>
          </v-col>
          <v-col cols="12" md="4">
            <v-menu
              v-model="dateMenuFrom"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-model="guide.valid_from"
                  label="Vigência (Início)"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="props"
                ></v-text-field>
              </template>
              <v-date-picker v-model="guide.valid_from" @update:model-value="dateMenuFrom = false"></v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="12" md="4">
            <v-menu
              v-model="dateMenuTo"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-model="guide.valid_to"
                  label="Vigência (Fim)"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="props"
                ></v-text-field>
              </template>
              <v-date-picker v-model="guide.valid_to" @update:model-value="dateMenuTo = false"></v-date-picker>
            </v-menu>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <v-btn type="submit" color="primary">Salvar</v-btn>
            <v-btn to="/guides" class="ml-2">Cancelar</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '@/services/api';
import { useClinicStore } from '@/stores/clinic';

// Interfaces
interface Clinic {
  id: string;
  name: string;
}

interface Patient {
  id: string;
  full_name: string;
  clinic: Clinic;
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

interface Guide {
  patient: string | null;
  clinic: string | null;
  clinic_name: string;
  payer: string | null;
  guide_type: string | null;
  nature: 'CHRONIC' | 'ACUTE';
  authorization_number: string;
  status: string | null;
  valid_from: string | null;
  valid_to: string | null;
}

const route = useRoute();
const router = useRouter();
const clinicStore = useClinicStore();

const form = ref<{ validate: () => Promise<{ valid: boolean }> } | null>(null);
const guide = ref<Guide>({
  patient: null,
  clinic: null,
  clinic_name: '',
  payer: null,
  guide_type: null,
  nature: 'CHRONIC',
  authorization_number: '',
  status: null,
  valid_from: null,
  valid_to: null,
});

// Data for select boxes
const patients = ref<Patient[]>([]);
const payers = ref<Payer[]>([]);
const guideTypes = ref<GuideType[]>([]);
const statuses = ref<ProcedureStatus[]>([]);
const natureOptions = ref([
    { title: 'Crônico', value: 'CHRONIC' },
    { title: 'Agudo', value: 'ACUTE' }
]);

// Control for date pickers
const dateMenuFrom = ref(false);
const dateMenuTo = ref(false);

const formTitle = computed(() => (route.params.id ? 'Editar Guia' : 'Nova Guia'));
const requiredRule = (v: string | null) => !!v || 'Este campo é obrigatório';

watch(() => guide.value.patient, (patientId) => {
  if (patientId) {
    const selectedPatient = patients.value.find(p => p.id === patientId);
    if (selectedPatient) {
      guide.value.clinic = selectedPatient.clinic.id;
      guide.value.clinic_name = selectedPatient.clinic.name;
    }
  }
});

const fetchRelatedData = async () => {
  const clinicId = clinicStore.selectedClinic?.id;
  if (!clinicId) {
    console.error('Nenhuma clínica selecionada no formulário de guias.');
    // Opcional: redirecionar ou mostrar um erro mais visível
    return;
  }

  try {
    const [patientsRes, payersRes, guideTypesRes, statusRes] = await Promise.all([
      apiClient.get<Patient[]>('/api/pacientes/', { params: { clinic: clinicId } }),
      apiClient.get<Payer[]>('/api/payers/'),
      apiClient.get<GuideType[]>('/api/guide-types/'),
      apiClient.get<ProcedureStatus[]>('/api/procedure-statuses/'),
    ]);
    patients.value = patientsRes.data;
    payers.value = payersRes.data;
    guideTypes.value = guideTypesRes.data;
    statuses.value = statusRes.data;
  } catch (error) {
    console.error('Erro ao buscar dados relacionados:', error);
  }
};

onMounted(async () => {
  await fetchRelatedData();
  if (route.params.id) {
    try {
      const response = await apiClient.get<any>(`/api/guias/${route.params.id}/`);
      const data = response.data;
      guide.value = {
        ...data,
        patient: data.patient.id,
        payer: data.payer.id,
        guide_type: data.guide_type.id,
        status: data.status.id,
        clinic_name: data.clinic.name,
      };
    } catch (error) {
      console.error('Erro ao buscar guia:', error);
    }
  }
});

const saveGuide = async () => {
  if (!form.value) return;
  const { valid } = await form.value.validate();
  if (!valid) return;

  try {
    if (route.params.id) {
      await apiClient.put(`/api/guias/${route.params.id}/`, guide.value);
    } else {
      await apiClient.post('/api/guias/', guide.value);
    }
    router.push('/guides');
  } catch (error) {
    console.error('Erro ao salvar guia:', error);
  }
};
</script>