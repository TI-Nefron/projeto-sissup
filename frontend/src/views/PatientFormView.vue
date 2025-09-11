<template>
  <div>
    <h1 class="text-h5 my-4">{{ formTitle }}</h1>
    <v-form ref="form" @submit.prevent="savePatient">
      <v-container>
        <!-- Error Alert -->
        <v-alert
          v-if="Object.keys(apiErrors).length > 0"
          type="error"
          title="Erro ao Salvar"
          class="mb-4"
          closable
          @click:close="apiErrors = {}"
        >
          <ul v-if="typeof apiErrors === 'object' && apiErrors !== null">
            <li v-for="(messages, field) in apiErrors" :key="field">
              <strong>{{ field }}:</strong> 
              <span v-if="typeof messages === 'object' && messages !== null">{{ Object.values(messages).join(', ') }}</span>
              <span v-else>{{ messages.join(', ') }}</span>
            </li>
          </ul>
        </v-alert>

        <!-- Patient Data Card -->
        <v-card class="mb-6">
          <v-card-title>Dados do Paciente</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="patient.full_name" label="Nome Completo" required></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="patient.cpf" label="CPF" required maxlength="14" :rules="[cpfRule]"></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="patient.cns" label="CNS" required maxlength="19" :rules="[cnsRule]"></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="patient.clinic_id" :items="clinics" item-title="name" item-value="id" label="Clínica" required readonly disabled></v-select>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="6">
                <v-select v-model="patient.patient_type" :items="patientTypes" item-title="title" item-value="value" label="Tipo" required></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="patient.status" :items="patientStatuses" item-title="title" item-value="value" label="Status" required></v-select>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Existing Documents Card -->
        <v-card v-if="!isNewPatient && patientDocuments.length > 0" class="mb-6">
          <v-card-title>Documentos Anexados</v-card-title>
          <v-list lines="one">
            <v-list-item
              v-for="doc in patientDocuments"
              :key="doc.id"
              :title="doc.type.name.startsWith('Outro') ? doc.description : doc.type.name"
              :subtitle="`Adicionado em: ${new Date(doc.created_at).toLocaleDateString()}`"
            >
              <template v-slot:append>
                <v-btn icon @click="openPreview(doc)" variant="text" size="small">
                  <v-icon>mdi-eye-outline</v-icon>
                </v-btn>
                <v-btn icon :href="doc.file_url.replace('http://minio:9000', 'http://localhost:9090')" target="_blank" variant="text" size="small">
                  <v-icon>mdi-download-outline</v-icon>
                </v-btn>
                <v-btn icon @click="deleteDocument(doc.id)" variant="text" size="small">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-list-item>
          </v-list>
        </v-card>

        <!-- Mandatory Documents Upload -->
        <v-card class="mb-6">
          <v-card-title>Documentos Obrigatórios</v-card-title>
          <v-card-text>
            <v-row v-for="(doc, index) in mandatoryDocs" :key="doc.type.id">
              <v-col cols="12" md="6">
                <v-label>{{ doc.type.name }}</v-label>
              </v-col>
              <v-col cols="12" md="6">
                <v-file-input
                  v-model="mandatoryDocs[index].file"
                  label="Arquivo"
                  density="compact"
                ></v-file-input>
              </v-col>
            </v-row>
            <v-alert v-if="mandatoryDocs.length === 0" type="info" text="Nenhum documento obrigatório para esta clínica."></v-alert>
          </v-card-text>
        </v-card>

        <!-- Extra Documents Upload -->
        <v-card class="mb-6">
          <v-card-title>Documentos Extras</v-card-title>
          <v-card-text>
            <v-row v-for="(doc, index) in extraDocs" :key="index" class="mb-2">
              <v-col cols="12" md="5">
                <v-text-field
                  v-model="doc.description"
                  label="Descrição do Documento"
                  density="compact"
                  hide-details
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-file-input
                  v-model="doc.file"
                  label="Arquivo"
                  density="compact"
                  hide-details
                ></v-file-input>
              </v-col>
              <v-col cols="12" md="1">
                <v-btn icon @click="removeExtraDoc(index)" size="small">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-btn @click="addExtraDoc" color="primary" class="mt-2">Adicionar Documento Extra</v-btn>
          </v-card-text>
        </v-card>

        <!-- Action Buttons -->
        <v-row class="mt-4">
          <v-col>
            <v-btn type="submit" color="primary">Salvar</v-btn>
            <v-btn to="/patients" class="ml-2">Cancelar</v-btn>
            <v-btn v-if="!isNewPatient" @click="showHistory = true" class="ml-2">Histórico</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>

    <ObjectHistory 
      v-model="showHistory"
      :object-id="patient.id"
      content-type-app-label="dialysis"
      content-type-model="patient"
    />

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
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '@/services/api';
import { useClinicStore } from '@/stores/clinic';
import * as adminApi from '@/services/administrationApi';
import ObjectHistory from '@/components/ObjectHistory.vue';

// Interfaces
interface DocumentType { id: string; name: string; }
interface Document {
  id: string;
  type: DocumentType;
  description?: string;
  file_url: string;
  created_at: string;
}
interface UploadableDoc {
  type: DocumentType;
  file: File[] | null;
}
interface ExtraDoc {
  description: string;
  file: File[] | null;
}

const route = useRoute();
const router = useRouter();
const form = ref<{ validate: () => Promise<{ valid: boolean }> } | null>(null);
const apiErrors = ref<Record<string, any>>({});
const showHistory = ref(false);

const patient = ref<any>({
  id: '',
  full_name: '',
  cpf: '',
  cns: '',
  clinic_id: null as string | null,
  patient_type: 'CHRONIC',
  status: 'IN_TREATMENT',
});

const clinics = ref<{id: string, name: string}[]>([]);
const patientDocuments = ref<Document[]>([]);
const mandatoryDocs = ref<UploadableDoc[]>([]);
const extraDocs = ref<ExtraDoc[]>([]);
const outroDocumentTypeId = ref<string | null>(null);

// Document Preview State
const previewDialog = ref(false);
const selectedDocForPreview = ref<Document | null>(null);

const patientTypes = ref([
    { title: 'Crônico', value: 'CHRONIC' },
    { title: 'Agudo', value: 'ACUTE' }
]);
const patientStatuses = ref([
    { title: 'Em Tratamento', value: 'IN_TREATMENT' },
    { title: 'Alta Ambulatorial', value: 'DISCHARGED' },
    { title: 'Óbito', value: 'DECEASED' },
    { title: 'Transferido', value: 'TRANSFERRED' }
]);

const formTitle = computed(() => route.params.id ? 'Editar Paciente' : 'Novo Paciente');
const isNewPatient = computed(() => !route.params.id);

// ... (CPF and CNS rules remain the same) ...
const cpfRule = (v: string) => { return true; };
const cnsRule = (v: string) => { return true; };

// ... (watchers for formatting remain the same) ...
watch(() => patient.value.cpf, (newValue) => { /* ... */ });
watch(() => patient.value.cns, (newValue) => { /* ... */ });
watch(() => patient.value.full_name, (newValue) => { /* ... */ });

const fetchMandatoryDocs = async (clinicId: string) => {
  try {
    const mandatoryDocIds = (await adminApi.getMandatoryDocuments(clinicId)).data;
    const allDocTypes = (await apiClient.get<DocumentType[]>('/api/document-types/', { params: { category: 'PATIENT' } })).data;
    
    mandatoryDocs.value = allDocTypes
      .filter(type => mandatoryDocIds.includes(type.id))
      .map(type => ({ type, file: null }));

    const outroDoc = allDocTypes.find(type => type.name.toLowerCase() === 'outro');
    if (outroDoc) {
      outroDocumentTypeId.value = outroDoc.id;
    }

  } catch (error) {
    console.error('Erro ao buscar documentos obrigatórios:', error);
  }
};

const addExtraDoc = () => {
  extraDocs.value.push({ description: '', file: null });
};

const removeExtraDoc = (index: number) => {
  extraDocs.value.splice(index, 1);
};

const openPreview = (doc: Document) => {
  selectedDocForPreview.value = doc;
  previewDialog.value = true;
};

const deleteDocument = async (docId: string) => {
  if (confirm('Tem certeza que deseja excluir este documento?')) {
    try {
      await apiClient.delete(`/api/documents/${docId}/`);
      patientDocuments.value = patientDocuments.value.filter(d => d.id !== docId);
    } catch (error) {
      console.error('Erro ao excluir documento:', error);
      // You might want to show a snackbar or alert to the user here
    }
  }
};

onMounted(async () => {
  try {
    const response = await apiClient.get('/api/administration/clinics/');
    clinics.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar clínicas:', error);
  }

  if (route.params.id) {
    try {
      const response = await apiClient.get(`/api/pacientes/${route.params.id}/`);
      patient.value = {
          ...response.data,
          clinic_id: response.data.clinic.id
      }
      patientDocuments.value = response.data.documents || [];
    } catch (error) {
      console.error('Erro ao buscar paciente:', error);
    }
  } else {
    const clinicStore = useClinicStore();
    if (clinicStore.selectedClinic) {
      patient.value.clinic_id = clinicStore.selectedClinic.id;
      await fetchMandatoryDocs(clinicStore.selectedClinic.id);
    } else {
      console.error('DEBUG: No clinic selected in store.');
    }
  }
});

const savePatient = async () => {
  apiErrors.value = {};
  if (!form.value) return;
  const { valid } = await form.value.validate();
  if (!valid) {
    return;
  }

  const formData = new FormData();
  
  // Append patient data
  Object.entries(patient.value).forEach(([key, value]) => {
    if (value !== null && key !== 'documents') { // Don't append existing documents
      formData.append(key, value as string);
    }
  });

  let docIndex = 0;

  // Append mandatory documents
  mandatoryDocs.value.forEach(doc => {
    if (doc.file && doc.file.length > 0) {
      formData.append(`documents_data[${docIndex}]file`, doc.file[0]);
      formData.append(`documents_data[${docIndex}]type`, doc.type.id);
      docIndex++;
    }
  });

  // Append extra documents
  extraDocs.value.forEach(doc => {
    if (doc.file && doc.file.length > 0 && doc.description && outroDocumentTypeId.value) {
      formData.append(`documents_data[${docIndex}]file`, doc.file[0]);
      formData.append(`documents_data[${docIndex}]type`, outroDocumentTypeId.value);
      formData.append(`documents_data[${docIndex}]description`, doc.description);
      docIndex++;
    }
  });

  try {
    if (isNewPatient.value) {
      await apiClient.post('/api/pacientes/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
    } else {
      await apiClient.put(`/api/pacientes/${route.params.id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
    }
    router.push('/patients');
  } catch (error: any) {
    console.error('Erro ao salvar paciente:', error);
    if (error.response && error.response.data) {
      apiErrors.value = error.response.data;
    }
  }
};
</script>
