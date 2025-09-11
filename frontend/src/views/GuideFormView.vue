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

        <!-- Existing Documents Card -->
        <v-card v-if="!isNewGuide && guideDocuments.length > 0" class="mb-6">
          <v-card-title>Documentos Anexados</v-card-title>
          <v-list lines="one">
            <v-list-item
              v-for="doc in guideDocuments"
              :key="doc.id"
              :title="doc.type.name.startsWith('Outro') ? doc.description : doc.type.name"
              :subtitle="`Adicionado em: ${new Date(doc.created_at).toLocaleDateString()}`"
            >
              <template v-slot:append>
                <v-btn icon @click="openPreview(doc)" variant="text" size="small"><v-icon>mdi-eye-outline</v-icon></v-btn>
                <v-btn icon :href="doc.file_url.replace('http://minio:9000', 'http://localhost:9090')" target="_blank" variant="text" size="small"><v-icon>mdi-download-outline</v-icon></v-btn>
                <v-btn icon @click="deleteDocument(doc.id)" variant="text" size="small"><v-icon>mdi-delete</v-icon></v-btn>
              </template>
            </v-list-item>
          </v-list>
        </v-card>

        <!-- Mandatory Documents Upload -->
        <v-card class="mb-6">
          <v-card-title>Documentos Obrigatórios</v-card-title>
          <v-card-text>
            <v-row v-for="(doc, index) in mandatoryDocs" :key="doc.type.id">
              <v-col cols="12" md="6"><v-label>{{ doc.type.name }}</v-label></v-col>
              <v-col cols="12" md="6"><v-file-input v-model="mandatoryDocs[index].file" label="Arquivo" density="compact"></v-file-input></v-col>
            </v-row>
            <v-alert v-if="!isNewGuide && mandatoryDocs.length === 0" type="info" text="Nenhum documento obrigatório para esta combinação."></v-alert>
            <v-alert v-if="isNewGuide && !guide.payer || !guide.guide_type || !guide.nature" type="info" text="Selecione convênio, tipo de guia e natureza para ver os documentos obrigatórios."></v-alert>
          </v-card-text>
        </v-card>

        <!-- Extra Documents Upload -->
        <v-card class="mb-6">
          <v-card-title>Documentos Extras</v-card-title>
          <v-card-text>
            <v-row v-for="(doc, index) in extraDocs" :key="index" class="mb-2">
              <v-col cols="12" md="5"><v-text-field v-model="doc.description" label="Descrição do Documento" density="compact" hide-details></v-text-field></v-col>
              <v-col cols="12" md="6"><v-file-input v-model="doc.file" label="Arquivo" density="compact" hide-details></v-file-input></v-col>
              <v-col cols="12" md="1"><v-btn icon @click="removeExtraDoc(index)" size="small"><v-icon>mdi-delete</v-icon></v-btn></v-col>
            </v-row>
            <v-btn @click="addExtraDoc" color="primary" class="mt-2">Adicionar Documento Extra</v-btn>
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

    <ObjectHistory v-model="showHistory" :object-id="guide.id" content-type-app-label="billing" content-type-model="guide" />
    <v-dialog v-model="previewDialog" fullscreen>
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="previewDialog = false"><v-icon>mdi-close</v-icon></v-btn>
          <v-toolbar-title>{{ selectedDocForPreview?.type.name }}</v-toolbar-title>
        </v-toolbar>
        <v-card-text class="pa-0" style="height: calc(100vh - 64px);"><embed v-if="selectedDocForPreview" :src="selectedDocForPreview.file_url.replace('http://minio:9000', 'http://localhost:9090')" type="application/pdf" width="100%" height="100%" /></v-card-text>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '@/services/api';
import { useClinicStore } from '@/stores/clinic';
import ObjectHistory from '@/components/ObjectHistory.vue';
import { debounce } from 'lodash-es';

// Interfaces
interface DocumentType { id: string; name: string; }
interface Document { id: string; type: DocumentType; description?: string; file_url: string; created_at: string; }
interface Clinic { id: string; name: string; }
interface Patient { id: string; full_name: string; clinic: Clinic; }
interface Payer { id: string; name: string; }
interface GuideType { id: string; name: string; }
interface ProcedureStatus { id: string; name: string; }
interface ParameterRule { id: string; required_documents: DocumentType[]; }
interface UploadableDoc { type: DocumentType; file: File[] | null; }
interface ExtraDoc { description: string; file: File[] | null; }
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
  documents: Document[];
}

const route = useRoute();
const router = useRouter();
const clinicStore = useClinicStore();

const form = ref<{ validate: () => Promise<{ valid: boolean }> } | null>(null);
const guide = ref<Guide>({ id: '', patient: null, clinic: null, clinic_name: '', payer: null, guide_type: null, nature: 'CHRONIC', authorization_number: '', status: null, valid_from: null, valid_to: null, documents: [] });
const showHistory = ref(false);

// Data for select boxes
const patients = ref<Patient[]>([]);
const payers = ref<Payer[]>([]);
const guideTypes = ref<GuideType[]>([]);
const statuses = ref<ProcedureStatus[]>([]);
const natureOptions = ref([{ title: 'Crônico', value: 'CHRONIC' }, { title: 'Agudo', value: 'ACUTE' }]);

// Document state
const guideDocuments = ref<Document[]>([]);
const mandatoryDocs = ref<UploadableDoc[]>([]);
const extraDocs = ref<ExtraDoc[]>([]);
const outroDocumentTypeId = ref<string | null>(null);
const previewDialog = ref(false);
const selectedDocForPreview = ref<Document | null>(null);

const formTitle = computed(() => (route.params.id ? 'Editar Guia' : 'Nova Guia'));
const isNewGuide = computed(() => !route.params.id);
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

const fetchMandatoryDocsForGuide = async () => {
  if (!guide.value.payer || !guide.value.guide_type || !guide.value.nature) {
    mandatoryDocs.value = [];
    return;
  }
  try {
    const params = { payer: guide.value.payer, guide_type: guide.value.guide_type, nature: guide.value.nature };
    const response = await apiClient.get<ParameterRule[]>('/api/parameters/parameter-rules/', { params });
    if (response.data.length > 0) {
      mandatoryDocs.value = response.data[0].required_documents.map(type => ({ type, file: null }));
    } else {
      mandatoryDocs.value = [];
    }
  } catch (error) {
    console.error('Erro ao buscar regras de parâmetros:', error);
    mandatoryDocs.value = [];
  }
};

const debouncedFetchMandatoryDocs = debounce(fetchMandatoryDocsForGuide, 500);
watch(() => [guide.value.payer, guide.value.guide_type, guide.value.nature], debouncedFetchMandatoryDocs);

const fetchRelatedData = async () => {
  const clinicId = clinicStore.selectedClinic?.id;
  if (!clinicId) return;

  try {
    const [patientsRes, payersRes, guideTypesRes, statusRes, allDocTypesRes] = await Promise.all([
      apiClient.get<Patient[]>(`/api/pacientes/`, { params: { clinic: clinicId } }),
      apiClient.get<Payer[]>(`/api/billing/clinics/${clinicId}/payers/`),
      apiClient.get<GuideType[]>(`/api/parameters/clinics/${clinicId}/guide-types/`),
      apiClient.get<ProcedureStatus[]>(`/api/parameters/clinics/${clinicId}/procedure-statuses/`),
      apiClient.get<DocumentType[]>('/api/document-types/', { params: { category: 'GUIDE' } })
    ]);
    patients.value = patientsRes.data;
    payers.value = payersRes.data;
    guideTypes.value = guideTypesRes.data;
    statuses.value = statusRes.data;
    const outroDoc = allDocTypesRes.data.find(type => type.name.toLowerCase() === 'outro');
    if (outroDoc) outroDocumentTypeId.value = outroDoc.id;

  } catch (error) { console.error('Erro ao buscar dados relacionados:', error); }
};

onMounted(async () => {
  await fetchRelatedData();
  if (route.params.id) {
    try {
      const response = await apiClient.get<Guide>(`/api/billing/guides/${route.params.id}/`);
      guide.value = { ...response.data, patient: response.data.patient.id, payer: response.data.payer.id, guide_type: response.data.guide_type.id, status: response.data.status.id, clinic_name: response.data.clinic.name };
      guideDocuments.value = response.data.documents || [];
    } catch (error) { console.error('Erro ao buscar guia:', error); }
  } else if (clinicStore.selectedClinic) {
    guide.value.clinic = clinicStore.selectedClinic.id;
    guide.value.clinic_name = clinicStore.selectedClinic.name || '';
  }
});

const addExtraDoc = () => extraDocs.value.push({ description: '', file: null });
const removeExtraDoc = (index: number) => extraDocs.value.splice(index, 1);
const openPreview = (doc: Document) => { selectedDocForPreview.value = doc; previewDialog.value = true; };

const deleteDocument = async (docId: string) => {
  if (confirm('Tem certeza que deseja excluir este documento?')) {
    try {
      await apiClient.delete(`/api/documents/${docId}/`);
      guideDocuments.value = guideDocuments.value.filter(d => d.id !== docId);
    } catch (error) { console.error('Erro ao excluir documento:', error); }
  }
};

const saveGuide = async () => {
  if (!form.value) return;
  const { valid } = await form.value.validate();
  if (!valid) return;

  const formData = new FormData();
  Object.entries(guide.value).forEach(([key, value]) => {
    if (value !== null && key !== 'documents') formData.append(key, value as string);
  });

  let docIndex = 0;
  mandatoryDocs.value.forEach(doc => {
    if (doc.file && doc.file.length > 0) {
      formData.append(`documents_data[${docIndex}]file`, doc.file[0]);
      formData.append(`documents_data[${docIndex}]type`, doc.type.id);
      docIndex++;
    }
  });
  extraDocs.value.forEach(doc => {
    if (doc.file && doc.file.length > 0 && doc.description && outroDocumentTypeId.value) {
      formData.append(`documents_data[${docIndex}]file`, doc.file[0]);
      formData.append(`documents_data[${docIndex}]type`, outroDocumentTypeId.value);
      formData.append(`documents_data[${docIndex}]description`, doc.description);
      docIndex++;
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
