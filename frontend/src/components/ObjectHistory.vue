<template>
  <v-dialog v-model="dialog" max-width="1000px">
    <v-card>
      <v-card-title>
        <span class="text-h5">Histórico de Alterações</span>
      </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="logs"
          :loading="loading"
          class="elevation-1"
        >
          <template v-slot:item.timestamp="{ item }">
            {{ new Date(item.raw.timestamp).toLocaleString() }}
          </template>
          <template v-slot:item.user="{ item }">
            {{ item.raw.user?.username || 'Sistema' }}
          </template>
          <template v-slot:item.action="{ item }">
            <v-chip :color="getActionColor(item.raw.action)" small>{{ item.raw.action }}</v-chip>
          </template>
          <template v-slot:item.changes="{ item }">
            <pre>{{ item.raw.changes }}</pre>
          </template>
        </v-data-table>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue-darken-1" text @click="dialog = false">Fechar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import apiClient from '@/services/api';

const props = defineProps({
  modelValue: Boolean,
  contentTypeAppLabel: String,
  contentTypeModel: String,
  objectId: String,
});

const emit = defineEmits(['update:modelValue']);

const dialog = ref(props.modelValue);
const logs = ref([]);
const loading = ref(false);
const contentTypeId = ref<number | null>(null);

const headers = ref([
  { title: 'Timestamp', key: 'timestamp' },
  { title: 'Usuário', key: 'user' },
  { title: 'Ação', key: 'action' },
  { title: 'Alterações', key: 'changes' },
]);

watch(() => props.modelValue, (newValue) => {
  dialog.value = newValue;
  if (newValue) {
    fetchContentTypeId().then(() => fetchHistory());
  }
});

watch(dialog, (newValue) => {
  if (!newValue) {
    emit('update:modelValue', false);
  }
});

const fetchContentTypeId = async () => {
  if (!props.contentTypeAppLabel || !props.contentTypeModel) return;
  try {
    const response = await apiClient.get('/api/audit/content-type/', {
      params: {
        app_label: props.contentTypeAppLabel,
        model: props.contentTypeModel,
      },
    });
    contentTypeId.value = response.data.id;
  } catch (error) {
    console.error('Erro ao buscar content type id:', error);
  }
};

const fetchHistory = async () => {
  if (!contentTypeId.value || !props.objectId) return;
  loading.value = true;
  try {
    const response = await apiClient.get('/api/audit/logs/', {
      params: {
        content_type: contentTypeId.value,
        object_id: props.objectId,
      },
    });
    logs.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar histórico:', error);
  } finally {
    loading.value = false;
  }
};

const getActionColor = (action: string) => {
  switch (action) {
    case 'CREATE': return 'green';
    case 'UPDATE': return 'orange';
    case 'DELETE': return 'red';
    default: return 'grey';
  }
};
</script>

<style scoped>
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
}
</style>
