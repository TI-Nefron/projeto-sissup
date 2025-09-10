<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="text-h5">Novo Registro de Histórico</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-autocomplete
            v-model="record.patient"
            :items="patients"
            item-title="full_name"
            item-value="id"
            label="Paciente"
            :rules="[requiredRule]"
          ></v-autocomplete>

          <v-select
            v-model="record.record_type"
            :items="recordTypes"
            item-title="title"
            item-value="value"
            label="Tipo de Registro"
            :rules="[requiredRule]"
          ></v-select>

          <v-text-field
            v-model="record.record_date"
            label="Data do Registro"
            type="date"
            :rules="[requiredRule]"
          ></v-text-field>

          <v-select
            v-model="record.clinic"
            :items="clinics"
            item-title="name"
            item-value="id"
            label="Clínica"
            :rules="[requiredRule]"
            readonly
            disabled
          ></v-select>

          <v-select
            v-if="record.record_type === 'SAIDA'"
            v-model="record.exit_type"
            :items="exitTypes"
            item-title="name"
            item-value="id"
            label="Tipo de Saída"
            :rules="[requiredRule]"
          ></v-select>

          <v-textarea v-model="record.notes" label="Observações"></v-textarea>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="$emit('update:modelValue', false)">Cancelar</v-btn>
        <v-btn color="primary" @click="save">Salvar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, defineEmits, defineProps, watch } from 'vue';
import apiClient from '@/services/api';
import { useClinicStore } from '@/stores/clinic';

const props = defineProps<{ modelValue: boolean }>();
const emit = defineEmits(['update:modelValue', 'save']);
const clinicStore = useClinicStore();

const form = ref<{ validate: () => Promise<{ valid: boolean }> } | null>(null);
const record = ref({
  patient: null,
  record_type: null,
  record_date: null,
  clinic: null,
  exit_type: null,
  notes: ''
});

const patients = ref([]);
const clinics = ref([]);
const recordTypes = ref([
  { title: 'Entrada', value: 'ENTRADA' },
  { title: 'Saída', value: 'SAIDA' },
]);
const exitTypes = ref([]);

const requiredRule = (v: any) => !!v || 'Este campo é obrigatório';

const fetchRelatedData = async () => {
  try {
    const [patientRes, clinicRes, exitTypeRes] = await Promise.all([
      apiClient.get('/api/pacientes/'),
      apiClient.get('/api/clinics/'),
      apiClient.get('/api/tipos-de-saida/'),
    ]);
    patients.value = patientRes.data;
    clinics.value = clinicRes.data;
    exitTypes.value = exitTypeRes.data;
  } catch (error) {
    console.error('Erro ao buscar dados para o formulário:', error);
  }
};

onMounted(fetchRelatedData);

const save = async () => {
  if (!form.value) return;
  const { valid } = await form.value.validate();
  if (!valid) return;

  try {
    await apiClient.post('/api/historico/', record.value);
    emit('save');
  } catch (error) {
    console.error('Erro ao salvar registro de histórico:', error);
  }
};
</script>
