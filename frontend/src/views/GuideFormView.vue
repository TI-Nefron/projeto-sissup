<template>
  <v-container>
    <h1 class="text-h5 my-4">{{ formTitle }}</h1>
    <v-form ref="form" @submit.prevent="saveGuide">
      <v-container>
        <!-- Guide Data Card -->
        <v-card class="mb-6">
          <v-card-title>Dados da Guia</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-autocomplete v-model="guide.patient" :items="patients" item-title="full_name" item-value="id" label="Paciente" required :rules="[requiredRule]"></v-autocomplete>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="guide.clinic_name" label="Clínica" readonly disabled></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="6">
                <v-select v-model="guide.payer" :items="payers" item-title="name" item-value="id" label="Convênio" required :rules="[requiredRule]"></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="guide.guide_type" :items="guideTypes" item-title="name" item-value="id" label="Tipo de Guia" required :rules="[requiredRule]"></v-select>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="6">
                <v-select v-model="guide.nature" :items="natureOptions" item-title="title" item-value="value" label="Natureza" required :rules="[requiredRule]"></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="guide.authorization_number" label="Número da Autorização"></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="4">
                <v-select v-model="guide.status" :items="statuses" item-title="name" item-value="id" label="Status" required :rules="[requiredRule]"></v-select>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field v-model="guide.valid_from" label="Vigência (Início)" type="date"></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field v-model="guide.valid_to" label="Vigência (Fim)" type="date"></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Mandatory Documents Card -->
        <v-card v-if="isNewGuide && mandatoryDocs.length > 0">
          <v-card-title>Documentos Obrigatórios</v-card-title>
          <v-card-text>
            <v-row>
              <v-col v-for="doc in mandatoryDocs" :key="doc.id" cols="12" md="6">
                <v-file-input
                  v-model="uploadedFiles[doc.id]"
                  :label="doc.name"
                  :rules="[v => !!v || 'Este documento é obrigatório']"
                  required
                  variant="outlined"
                  density="compact"
                ></v-file-input>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Action Buttons -->
        <v-row class="mt-4">
          <v-col>
            <v-btn type="submit" color="primary" :disabled="isSaveDisabled">Salvar</v-btn>
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
import * as adminApi from '@/services/administrationApi';

// Interfaces
interface DocumentType { id: string; name: string; category: 'PATIENT' | 'GUIDE'; }
interface Clinic { id: string; name: string; }
interface Patient { id: string; full_name: string; clinic: Clinic; }
interface Payer { id: string; name: string; }
interface GuideType { id: string; name: string; }
interface ProcedureStatus { id: string; name: string; }
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
const guide = ref<Guide>({ patient: null, clinic: null, clinic_name: '', payer: null, guide_type: null, nature: 'CHRONIC', authorization_number: '', status: null, valid_from: null, valid_to: null });

// Data for select boxes
const patients = ref<Patient[]>([]);
const payers = ref<Payer[]>([]);
const guideTypes = ref<GuideType[]>([]);
const statuses = ref<ProcedureStatus[]>([]);
const natureOptions = ref([{ title: 'Crônico', value: 'CHRONIC' }, { title: 'Agudo', value: 'ACUTE' }]);

// Mandatory Docs
const mandatoryDocs = ref<DocumentType[]>([]);
const uploadedFiles = ref<Record<string, File[]>>({});

const formTitle = computed(() => (route.params.id ? 'Editar Guia' : 'Nova Guia'));
const isNewGuide = computed(() => !route.params.id);
const requiredRule = (v: string | null) => !!v || 'Este campo é obrigatório';

const isSaveDisabled = computed(() => {
  if (isNewGuide.value) {
    if (mandatoryDocs.value.length === 0) return false;
    const allFilesUploaded = mandatoryDocs.value.every(doc => uploadedFiles.value[doc.id] && uploadedFiles.value[doc.id].length > 0);
    return !allFilesUploaded;
  }
  return false;
});

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
  if (!clinicId) return;

  try {
    const [patientsRes, payersRes, guideTypesRes, statusRes] = await Promise.all([
      apiClient.get<Patient[]>(`/api/pacientes/`, { params: { clinic: clinicId } }),
      apiClient.get<Payer[]>(`/api/billing/clinics/${clinicId}/payers/`),
      apiClient.get<GuideType[]>(`/api/parameters/clinics/${clinicId}/guide-types/`),
      apiClient.get<ProcedureStatus[]>(`/api/parameters/clinics/${clinicId}/procedure-statuses/`),
    ]);
    patients.value = patientsRes.data;
    payers.value = payersRes.data;
    guideTypes.value = guideTypesRes.data;
    statuses.value = statusRes.data;
  } catch (error) { console.error('Erro ao buscar dados relacionados:', error); }
};

async function fetchMandatoryDocs(clinicId: string) {
  try {
    const allDocTypesResponse = await apiClient.get<DocumentType[]>('/api/document-types/');
    const mandatoryIdsResponse = await adminApi.getMandatoryDocuments(clinicId);
    
    const mandatoryIds = new Set(mandatoryIdsResponse.data);
    mandatoryDocs.value = allDocTypesResponse.data.filter(doc => 
      doc.category === 'GUIDE' && mandatoryIds.has(doc.id)
    );
  } catch (error) { console.error('Erro ao buscar documentos obrigatórios:', error); }
}

onMounted(async () => {
  const clinicId = clinicStore.selectedClinic?.id;
  await fetchRelatedData();

  if (route.params.id) {
    // Fetch existing guide data
    try {
      const response = await apiClient.get<any>(`/api/billing/guides/${route.params.id}/`);
      const data = response.data;
      guide.value = { ...data, patient: data.patient.id, payer: data.payer.id, guide_type: data.guide_type.id, status: data.status.id, clinic_name: data.clinic.name };
    } catch (error) { console.error('Erro ao buscar guia:', error); }
  } else if (clinicId) {
    // It's a new guide, fetch mandatory docs
    guide.value.clinic = clinicId;
    guide.value.clinic_name = clinicStore.selectedClinic?.name || '';
    await fetchMandatoryDocs(clinicId);
  }
});

const saveGuide = async () => {
  if (!form.value) return;
  const { valid } = await form.value.validate();
  if (!valid || isSaveDisabled.value) return;

  try {
    if (isNewGuide.value) {
      const formData = new FormData();
      Object.entries(guide.value).forEach(([key, value]) => {
        if (value !== null) formData.append(key, value as string);
      });

      Object.entries(uploadedFiles.value).forEach(([docId, fileList]) => {
        if (fileList && fileList.length > 0) formData.append(`files[${docId}]`, fileList[0]);
      });

      await apiClient.post('/api/billing/guides/', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
    } else {
      await apiClient.put(`/api/billing/guides/${route.params.id}/`, guide.value);
    }
    router.push('/guides');
  } catch (error) { console.error('Erro ao salvar guia:', error); }
};
</script>
