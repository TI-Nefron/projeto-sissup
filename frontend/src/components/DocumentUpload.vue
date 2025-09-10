<template>
  <v-form ref="form" v-model="valid">
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-select
            v-model="selectedDocumentType"
            :items="documentTypes"
            item-title="name"
            item-value="id"
            label="Tipo de Documento"
            :rules="[requiredRule]"
            required
          ></v-select>
        </v-col>
        <v-col v-if="showDescription" cols="12">
          <v-text-field
            v-model="description"
            label="Descrição do Documento"
            :rules="[requiredRule]"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12">
          <v-file-input
            v-model="selectedFile"
            label="Selecione o arquivo"
            :rules="[requiredRule]"
            required
          ></v-file-input>
        </v-col>
      </v-row>
      <v-btn
        @click="upload"
        :loading="loading"
        :disabled="!valid"
        color="primary"
        class="mt-4"
      >
        Enviar
      </v-btn>
      <v-alert v-if="message" :type="messageType" class="mt-4">{{ message }}</v-alert>
    </v-container>
  </v-form>
</template>

<script setup lang="ts">
import { ref, onMounted, defineProps, defineEmits, computed } from 'vue';
import apiClient from '@/services/api';

interface DocumentType {
  id: string;
  name: string;
}

const props = defineProps({
  content_type_str: { type: String, required: true },
  object_id: { type: String, required: true },
  clinic_id: { type: String, required: true },
});

const emit = defineEmits(['upload-completed']);

const form = ref<{ validate: () => Promise<{ valid: boolean }>; reset: () => void; } | null>(null);
const valid = ref(true);
const loading = ref(false);
const documentTypes = ref<DocumentType[]>([]);
const selectedDocumentType = ref<string | null>(null);
const description = ref('');
const selectedFile = ref<File | null>(null);
const message = ref<string | null>(null);
const messageType = ref<'success' | 'error'>('success');

const requiredRule = (v: any) => !!v || 'Este campo é obrigatório';

const showDescription = computed(() => {
  if (!selectedDocumentType.value) return false;
  const selectedType = documentTypes.value.find(t => t.id === selectedDocumentType.value);
  return selectedType?.name.startsWith('Outro') ?? false;
});

const fetchDocumentTypes = async () => {
  try {
    const response = await apiClient.get<DocumentType[]>('/api/document-types/');
    documentTypes.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar tipos de documento:', error);
  }
};

onMounted(fetchDocumentTypes);

const upload = async () => {
  if (!form.value) return;
  const { valid } = await form.value.validate();
  if (!valid || !selectedFile.value) return;

  loading.value = true;
  message.value = null;

  const formData = new FormData();
  formData.append('file', selectedFile.value);
  formData.append('type', selectedDocumentType.value!);
  formData.append('object_id', props.object_id);
  formData.append('content_type_str', props.content_type_str);
  formData.append('clinic', props.clinic_id);
  if (showDescription.value && description.value) {
    formData.append('description', description.value);
  }

  try {
    await apiClient.post('/api/documents/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    message.value = 'Arquivo enviado com sucesso!';
    messageType.value = 'success';
    emit('upload-completed');
    description.value = '';
    form.value.reset();
  } catch (error) {
    console.error('Erro ao enviar documento:', error);
    message.value = 'Erro ao enviar o arquivo.';
    messageType.value = 'error';
  } finally {
    loading.value = false;
  }
};
</script>