<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="payers"
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Convênios</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ props }">
              <v-btn color="primary" dark class="mb-2" v-bind="props">Novo Convênio</v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field v-model="editedItem.name" label="Nome do Convênio"></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-select
                        v-model="editedItem.payer_type"
                        :items="payerTypes"
                        label="Tipo"
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue-darken-1" text @click="close">Cancelar</v-btn>
                <v-btn color="blue-darken-1" text @click="save">Salvar</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="text-h5">Tem certeza que deseja remover este convênio?</v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue-darken-1" text @click="closeDelete">Cancelar</v-btn>
                <v-btn color="blue-darken-1" text @click="deleteItemConfirm">OK</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon size="small" class="me-2" @click="editItem(item)">mdi-pencil</v-icon>
        <v-icon size="small" @click="deleteItem(item)">mdi-delete</v-icon>
      </template>
      <template v-slot:item.is_active="{ value }">
        <v-chip :color="value ? 'green' : 'red'" :text="value ? 'Ativo' : 'Inativo'"></v-chip>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, nextTick } from 'vue';
import apiClient from '@/services/api';

interface Payer {
  id: string;
  name: string;
  payer_type: 'SUS' | 'PRIVATE';
  is_active: boolean;
}

const payers = ref<Payer[]>([]);
const loading = ref(true);
const dialog = ref(false);
const dialogDelete = ref(false);
const payerTypes = ref(['SUS', 'PRIVATE']);

const headers = ref([
  { title: 'Nome', value: 'name' },
  { title: 'Tipo', value: 'payer_type' },
  { title: 'Status', value: 'is_active' },
  { title: 'Ações', value: 'actions', sortable: false },
]);

const editedIndex = ref(-1);
const editedItem = ref<Partial<Payer>>({
  name: '',
  payer_type: 'PRIVATE',
  is_active: true,
});
const defaultItem = ref<Partial<Payer>>({
  name: '',
  payer_type: 'PRIVATE',
  is_active: true,
});

const formTitle = computed(() => (editedIndex.value === -1 ? 'Novo Convênio' : 'Editar Convênio'));

const fetchPayers = async () => {
  loading.value = true;
  try {
    const response = await apiClient.get('/api/payers/');
    payers.value = response.data;
  } catch (error) {
    console.error('Error fetching payers:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchPayers);

const editItem = (item: Payer) => {
  editedIndex.value = payers.value.findIndex(p => p.id === item.id);
  editedItem.value = { ...item };
  dialog.value = true;
};

const deleteItem = (item: Payer) => {
  editedIndex.value = payers.value.findIndex(p => p.id === item.id);
  editedItem.value = { ...item };
  dialogDelete.value = true;
};

const close = () => {
  dialog.value = false;
  nextTick(() => {
    editedItem.value = { ...defaultItem.value };
    editedIndex.value = -1;
  });
};

const closeDelete = () => {
  dialogDelete.value = false;
  nextTick(() => {
    editedItem.value = { ...defaultItem.value };
    editedIndex.value = -1;
  });
};

const save = async () => {
  try {
    if (editedIndex.value > -1) {
      await apiClient.put(`/api/payers/${editedItem.value.id}/`, editedItem.value);
    } else {
      await apiClient.post('/api/payers/', editedItem.value);
    }
    fetchPayers();
  } catch (error) {
    console.error('Error saving payer:', error);
  } finally {
    close();
  }
};

const deleteItemConfirm = async () => {
  try {
    await apiClient.delete(`/api/payers/${editedItem.value.id}/`);
    fetchPayers();
  } catch (error) {
    console.error('Error deleting payer:', error);
  } finally {
    closeDelete();
  }
};
</script>
