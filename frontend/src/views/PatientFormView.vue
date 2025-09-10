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

        <!-- Documents Card -->
        <v-card class="mb-6">
          <v-card-text>
            <MultiDocumentUpload 
              category="PATIENT" 
              @update:documents="updateDocuments"
            />
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

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '@/services/api';
import { useClinicStore } from '@/stores/clinic';
import MultiDocumentUpload from '@/components/MultiDocumentUpload.vue';
import ObjectHistory from '@/components/ObjectHistory.vue';

interface DocumentData {
  type: string | null;
  description: string;
  file: File[] | null;
}

const route = useRoute();
const router = useRouter();
const form = ref<{ validate: () => Promise<{ valid: boolean }> } | null>(null);
const apiErrors = ref<Record<string, any>>({});
const showHistory = ref(false);

const patient = ref({
  id: '',
  full_name: '',
  cpf: '',
  cns: '',
  clinic_id: null as string | null,
  patient_type: 'CHRONIC',
  status: 'IN_TREATMENT',
});

const clinics = ref<{id: string, name: string}[]>([]);
const documentsToUpload = ref<DocumentData[]>([]);

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

const updateDocuments = (docs: DocumentData[]) => {
  documentsToUpload.value = docs;
};

// ... (CPF and CNS rules remain the same) ...
const cpfRule = (v: string) => { return true; };
const cnsRule = (v: string) => { return true; };

// ... (watchers for formatting remain the same) ...
watch(() => patient.value.cpf, (newValue) => { /* ... */ });
watch(() => patient.value.cns, (newValue) => { /* ... */ });
watch(() => patient.value.full_name, (newValue) => { /* ... */ });

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
      const patientData = response.data;
      patient.value = {
          ...patientData,
          clinic_id: patientData.clinic.id
      }
    } catch (error) {
      console.error('Erro ao buscar paciente:', error);
    }
  } else {
    const clinicStore = useClinicStore();
    if (clinicStore.selectedClinic) {
      patient.value.clinic_id = clinicStore.selectedClinic.id;
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
    if (value !== null) {
      formData.append(key, value as string);
    }
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
    if (isNewPatient.value) {
      await apiClient.post('/api/pacientes/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    } else {
      await apiClient.put(`/api/pacientes/${route.params.id}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
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