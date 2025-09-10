<template>
  <v-container>
    <h1 class="text-h5 my-4">Logs de Auditoria</h1>
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
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getAuditLogs } from '@/services/auditApi';

const logs = ref([]);
const loading = ref(true);

const headers = ref([
  { title: 'Timestamp', key: 'timestamp' },
  { title: 'Usuário', key: 'user' },
  { title: 'Ação', key: 'action' },
  { title: 'Objeto', key: 'object_repr' },
  { title: 'Alterações', key: 'changes' },
]);

onMounted(async () => {
  try {
    const response = await getAuditLogs();
    logs.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar logs de auditoria:', error);
  } finally {
    loading.value = false;
  }
});

const getActionColor = (action: string) => {
  switch (action) {
    case 'CREATE': return 'green';
    case 'UPDATE': return 'orange';
    case 'DELETE': return 'red';
    default: return 'grey';
  }
};
</script>
