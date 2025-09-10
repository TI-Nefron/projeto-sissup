<template>
  <div>
    <h1 class="text-h5 my-4">{{ formTitle }}</h1>
    <v-form ref="form" @submit.prevent="savePatient">
      <v-container>
        <v-alert
          v-if="Object.keys(apiErrors).length > 0"
          type="error"
          title="Erro ao Salvar"
          class="mb-4"
          closable
          @click:close="apiErrors = {}"
        >
          <ul>
            <li v-for="(messages, field) in apiErrors" :key="field">
              <strong>{{ field }}:</strong> {{ messages.join(', ') }}
            </li>
          </ul>
        </v-alert>

        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="patient.full_name"
              label="Nome Completo"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="patient.cpf"
              label="CPF"
              required
              maxlength="14"
              :rules="[cpfRule]"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="patient.cns"
              label="CNS"
              required
              maxlength="19"
              :rules="[cnsRule]"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="patient.clinic_id"
              :items="clinics"
              item-title="name"
              item-value="id"
              label="Clínica"
              required
              :readonly="true"
              :disabled="true"
            ></v-select>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <v-select
              v-model="patient.patient_type"
              :items="patientTypes"
              item-title="title"
              item-value="value"
              label="Tipo"
              required
            ></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="patient.status"
              :items="patientStatuses"
              item-title="title"
              item-value="value"
              label="Status"
              required
            ></v-select>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-btn type="submit" color="primary">Salvar</v-btn>
            <v-btn to="/patients" class="ml-2">Cancelar</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '@/services/api';
import { useClinicStore } from '@/stores/clinic';

const route = useRoute();
const router = useRouter();
const form = ref<{ validate: () => Promise<{ valid: boolean }> } | null>(null);
const apiErrors = ref<Record<string, string[]>>({});

const patient = ref({
  full_name: '',
  cpf: '',
  cns: '',
  clinic_id: null,
  patient_type: 'CHRONIC',
  status: 'IN_TREATMENT',
});

const clinics = ref([]);
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

const formTitle = computed(() => {
  return route.params.id ? 'Editar Paciente' : 'Novo Paciente';
});

const cpfRule = (v: string) => {
    if (!v) return 'Este campo é obrigatório';
    const cleaned = v.replace(/\D/g, '');
    if (cleaned.length !== 11 || /^(\d)\1{10}$/.test(cleaned)) {
        return 'CPF inválido';
    }
    let sum = 0;
    let remainder;
    for (let i = 1; i <= 9; i++) {
        sum = sum + parseInt(cleaned.substring(i - 1, i)) * (11 - i);
    }
    remainder = (sum * 10) % 11;
    if ((remainder === 10) || (remainder === 11)) {
        remainder = 0;
    }
    if (remainder !== parseInt(cleaned.substring(9, 10))) {
        return 'CPF inválido';
    }
    sum = 0;
    for (let i = 1; i <= 10; i++) {
        sum = sum + parseInt(cleaned.substring(i - 1, i)) * (12 - i);
    }
    remainder = (sum * 10) % 11;
    if ((remainder === 10) || (remainder === 11)) {
        remainder = 0;
    }
    if (remainder !== parseInt(cleaned.substring(10, 11))) {
        return 'CPF inválido';
    }
    return true;
}

const cnsRule = (v: string) => {
    if (!v) return 'Este campo é obrigatório';
    const cns = v.replace(/\D/g, '');

    if (cns.length !== 15) {
        return 'CNS inválido';
    }

    if (['1', '2'].includes(cns.charAt(0))) {
        const pis = cns.substring(0, 11);
        let sum = 0;
        for (let i = 0; i < 11; i++) {
            sum += parseInt(pis.charAt(i), 10) * (15 - i);
        }
        const remainder = sum % 11;
        let dv = 11 - remainder;
        if (dv === 11) {
            dv = 0;
        }
        if (dv === 10) {
            sum = 0;
            for (let i = 0; i < 11; i++) {
                sum += parseInt(pis.charAt(i), 10) * (15 - i);
            }
            sum += 2;
            const remainder2 = sum % 11;
            dv = 11 - remainder2;
            return cns === `${pis}001${dv}`;
        }
        return cns === `${pis}000${dv}`;
    }

    if (['7', '8', '9'].includes(cns.charAt(0))) {
        let sum = 0;
        for (let i = 0; i < 15; i++) {
            sum += parseInt(cns.charAt(i), 10) * (15 - i);
        }
        return sum % 11 === 0 || 'CNS inválido';
    }

    return 'CNS inválido';
}

watch(() => patient.value.cpf, (newValue) => {
  if (newValue) {
    const cleaned = newValue.replace(/\D/g, '');
    let formatted = cleaned;
    if (cleaned.length > 3) {
      formatted = `${cleaned.slice(0, 3)}.${cleaned.slice(3)}`;
    }
    if (cleaned.length > 6) {
      formatted = `${formatted.slice(0, 7)}.${cleaned.slice(6)}`;
    }
    if (cleaned.length > 9) {
      formatted = `${formatted.slice(0, 11)}-${cleaned.slice(9)}`;
    }
    patient.value.cpf = formatted.slice(0, 14);
  }
});

watch(() => patient.value.cns, (newValue) => {
  if (newValue) {
    const cleaned = newValue.replace(/\D/g, '');
    let formatted = cleaned;
    if (cleaned.length > 3) {
      formatted = `${cleaned.slice(0, 3)}.${cleaned.slice(3)}`;
    }
    if (cleaned.length > 6) {
      formatted = `${formatted.slice(0, 7)}.${cleaned.slice(6)}`;
    }
    if (cleaned.length > 9) {
      formatted = `${formatted.slice(0, 11)}.${cleaned.slice(9)}`;
    }
    if (cleaned.length > 12) {
      formatted = `${formatted.slice(0, 15)}.${cleaned.slice(12)}`;
    }
    patient.value.cns = formatted.slice(0, 19);
  }
});

watch(() => patient.value.full_name, (newValue, oldValue) => {
  if (newValue) {
    // Remove accents
    let formatted = newValue.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    
    // Prevent multiple spaces
    formatted = formatted.replace(/\s{2,}/g, ' ');

    // Capitalize first letter of each word
    formatted = formatted.split(' ').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ');

    if (formatted !== newValue) {
      patient.value.full_name = formatted;
    }
  }
});


onMounted(async () => {
  try {
    const response = await apiClient.get('/api/clinics/');
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
    // Se é um novo paciente, preenche a clínica a partir da store
    const clinicStore = useClinicStore();
    if (clinicStore.selectedClinic) {
      patient.value.clinic_id = clinicStore.selectedClinic.id;
    }
  }
});

const savePatient = async () => {
  apiErrors.value = {}; // Limpa erros antigos
  if (!form.value) return;
  const { valid } = await form.value.validate();
  if (!valid) {
    return;
  }

  try {
    const dataToSave = { ...patient.value };
    
    // Remove a máscara dos campos antes de enviar
    dataToSave.cpf = dataToSave.cpf.replace(/\D/g, '');
    dataToSave.cns = dataToSave.cns.replace(/\D/g, '');

    const payload = dataToSave;

    if (route.params.id) {
      await apiClient.put(`/api/pacientes/${route.params.id}/`, payload);
    } else {
      await apiClient.post('/api/pacientes/', payload);
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