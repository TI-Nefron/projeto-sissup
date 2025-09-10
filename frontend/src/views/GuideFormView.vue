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

        <!-- Documents Card -->
        <v-card class="mb-6">
          <v-card-text>
            <MultiDocumentUpload 
              category="GUIDE" 
              @update:documents="updateDocuments"
            />
          </v-card-text>
        </v-card>

        <!-- Action Buttons -->
        <v-row class="mt-4">
          <v-col>
            <v-btn type="submit" color="primary">Salvar</v-btn>
            <v-btn to="/guides" class="ml-2">Cancelar</v-btn>
            <v-btn v-if="!isNewGuide" @click="showHistory = true" class="ml-2">Histórico</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>

    <ObjectHistory 
      v-model="showHistory"
      :object-id="guide.id"
      content-type-app-label="billing"
      content-type-model="guide"
    />

  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '@/services/api';
import { useClinicStore } from '@/stores/clinic';
import MultiDocumentUpload from '@/components/MultiDocumentUpload.vue';
import ObjectHistory from '@/components/ObjectHistory.vue';

// Interfaces
interface DocumentData {
  type: string | null;
  description: string;
  file: File[] | null;
}
interface Clinic { id: string; name: string; }
interface Patient { id: string; full_name: string; clinic: Clinic; }
interface Payer { id: string; name: string; }
interface GuideType { id: string; name: string; }
interface ProcedureStatus { id: string; name: string; }
interface Guide {
  id: string;
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
const guide = ref<Guide>({ id: '', patient: null, clinic: null, clinic_name: '', payer: null, guide_type: null, nature: 'CHRONIC', authorization_number: '', status: null, valid_from: null, valid_to: null });
const showHistory = ref(false);

// Data for select boxes
const patients = ref<Patient[]>([]);
const payers = ref<Payer[]>([]);
const guideTypes = ref<GuideType[]>([]);
const statuses = ref<ProcedureStatus[]>([]);
const natureOptions = ref([{ title: 'Crônico', value: 'CHRONIC' }, { title: 'Agudo', value: 'ACUTE' }]);
const documentsToUpload = ref<DocumentData[]>([]);

const formTitle = computed(() => (route.params.id ? 'Editar Guia' : 'Nova Guia'));
const isNewGuide = computed(() => !route.params.id);
const requiredRule = (v: string | null) => !!v || 'Este campo é obrigatório';

const updateDocuments = (docs: DocumentData[]) => {
  documentsToUpload.value = docs;
};

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
    guide.value.clinic = clinicId;
    guide.value.clinic_name = clinicStore.selectedClinic?.name || '';
  }
});

const saveGuide = async () => {
  if (!form.value) return;
  const { valid } = await form.value.validate();
  if (!valid) return;

  const formData = new FormData();
  
  // Append guide data
  Object.entries(guide.value).forEach(([key, value]) => {
    if (value !== null) formData.append(key, value as string);
  });

  // Append documents
  documentsToUpload.value.forEach((doc, index) => {
    if (doc.file && doc.file.length > 0 && doc.type) {
      formData.append(`documents_data[${index}]file`, doc.file[0]);
      formData.append(`documents_data[${index}]type`, doc.type);
      if (doc.description) {
        formData.append(`documents_data[${index}]description`, doc.description);
      }
    }
  });

  try {
    if (isNewGuide.value) {
      await apiClient.post('/api/billing/guides/', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
    } else {
      await apiClient.put(`/api/billing/guides/${route.params.id}/`, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
    }
    router.push('/guides');
  } catch (error) { console.error('Erro ao salvar guia:', error); }
};
</script>
