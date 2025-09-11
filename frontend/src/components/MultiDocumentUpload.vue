<template>
  <v-container>
    <h3 class="text-h6 mb-4">Documentos</h3>

    <v-row v-for="(doc, index) in documents" :key="index" class="mb-4 align-center">
      <v-col cols="12" md="4">
        <v-select
          v-model="doc.type"
          :items="documentTypes"
          item-title="name"
          item-value="id"
          label="Tipo de Documento"
          density="compact"
          hide-details
        ></v-select>
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field
          v-if="showDescription(doc.type)"
          v-model="doc.description"
          label="Descrição"
          density="compact"
          hide-details
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="3">
        <v-file-input
          v-model="doc.file"
          label="Arquivo"
          density="compact"
          hide-details
          @change="(event) => handleFileChange(event, index)"
        ></v-file-input>
      </v-col>
      <v-col cols="12" md="1">
        <v-btn icon @click="removeDocument(index)" size="small">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <v-btn @click="addDocument" color="primary" class="mt-2">Adicionar Documento</v-btn>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, defineEmits, defineProps } from 'vue';
import apiClient from '@/services/api';

interface DocumentType {
  id: string;
  name: string;
}

interface DocumentData {
  type: string | null;
  description: string;
  file: File[] | null;
}

const props = defineProps({
  category: { type: String, required: true }, // 'PATIENT' or 'GUIDE'
});

const emit = defineEmits(['update:documents']);

const documents = ref<DocumentData[]>([]);
const documentTypes = ref<DocumentType[]>([]);

const fetchDocumentTypes = async () => {
  try {
    const response = await apiClient.get<DocumentType[]>('/api/document-types/', {
      params: { category: props.category },
    });
    // Standardize the name for the "Other" document type to keep the UI clean
    documentTypes.value = response.data.map(doc => {
      if (doc.name.includes('Outro')) {
        return { ...doc, name: 'Outro' };
      }
      return doc;
    });
  } catch (error) {
    console.error('Erro ao buscar tipos de documento:', error);
  }
};

onMounted(fetchDocumentTypes);

const addDocument = () => {
  documents.value.push({ type: null, description: '', file: null });
};

const removeDocument = (index: number) => {
  documents.value.splice(index, 1);
};

const handleFileChange = (event: Event, index: number) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    documents.value[index].file = [target.files[0]];
  } else {
    documents.value[index].file = null;
  }
};

const showDescription = (typeId: string | null) => {
  if (!typeId) return false;
  const selectedType = documentTypes.value.find(t => t.id === typeId);
  return selectedType?.name.toLowerCase().startsWith('outro') ?? false;
};

watch(documents, (newDocs) => {
  emit('update:documents', newDocs);
}, { deep: true });

</script>