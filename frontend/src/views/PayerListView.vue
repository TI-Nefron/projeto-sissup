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
                <v-form ref="form" v-model="valid">
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field
                          v-model="editedItem.name"
                          label="Nome do Convênio"
                          :rules="[requiredRule]"
                          required
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="8">
                        <v-select
                          v-model="editedItem.payer_type"
                          :items="payerTypes"
                          label="Tipo"
                          :rules="[requiredRule]"
                          required
                        ></v-select>
                      </v-col>
                      <v-col cols="12" sm="4">
                        <v-switch
                          v-model="editedItem.is_active"
                          label="Ativo"
                          color="primary"
                        ></v-switch>
                      </v-col>
                      <v-col cols="12">
                        <v-select
                          v-model="editedItem.clinics"
                          :items="clinics"
                          item-title="name"
                          item-value="id"
                          label="Clínicas"
                          multiple
                          chips
                          closable-chips
                        ></v-select>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue-darken-1" text @click="close">Cancelar</v-btn>
                <v-btn
                  color="blue-darken-1"
                  text
                  @click="save"
                  :loading="saveLoading"
                  :disabled="!valid"
                >Salvar</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="600px">
            <v-card>
              <v-card-title class="text-h5">Tem certeza que deseja remover o convênio "{{ editedItem.name }}"?</v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue-darken-1" text @click="closeDelete">Cancelar</v-btn>
                <v-btn color="red-darken-1" text @click="deleteItemConfirm">OK</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template #[`item.actions`]='{ item }'>
        <v-icon size="small" class="me-2" @click="editItem(item)">mdi-pencil</v-icon>
        <v-icon size="small" @click="deleteItem(item)">mdi-delete</v-icon>
      </template>
      <template #[`item.is_active`]='{ value }'>
        <v-chip :color="value ? 'green' : 'red'" :text="value ? 'Ativo' : 'Inativo'" size="small"></v-chip>
      </template>
    </v-data-table>

    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      timeout="3000"
    >
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, nextTick } from 'vue';
import apiClient from '@/services/api';

interface Clinic {
  id: string;
  name: string;
}

interface Payer {
  id: string;
  name: string;
  payer_type: 'SUS' | 'PRIVATE';
  is_active: boolean;
  clinics: string[];
}

const payers = ref<Payer[]>([]);
const loading = ref(true);
const saveLoading = ref(false);
const dialog = ref(false);
const dialogDelete = ref(false);
const form = ref<{ validate: () => Promise<{ valid: boolean }>; resetValidation: () => void; } | null>(null);
const valid = ref(true);
const payerTypes = ref(['SUS', 'PRIVATE']);
const clinics = ref<Clinic[]>([]);

// Snackbar state
const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('success');

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
  clinics: [],
});
const defaultItem = ref<Partial<Payer>>({
  name: '',
  payer_type: 'PRIVATE',
  is_active: true,
  clinics: [],
});

// Validation Rules
const requiredRule = (v: string) => !!v || 'Este campo é obrigatório';

const formTitle = computed(() => (editedIndex.value === -1 ? 'Novo Convênio' : 'Editar Convênio'));

const showSnackbar = (text: string, color: 'success' | 'error' = 'success') => {
  snackbarText.value = text;
  snackbarColor.value = color;
  snackbar.value = true;
};

const fetchPayers = async () => {
  loading.value = true;
  try {
    const response = await apiClient.get<Payer[]>('/api/payers/');
    payers.value = response.data;
  } catch (error) {
    console.error('Error fetching payers:', error);
    showSnackbar('Erro ao carregar convênios.', 'error');
  } finally {
    loading.value = false;
  }
};

const fetchClinics = async () => {
  try {
    const response = await apiClient.get<Clinic[]>('/api/clinics/');
    clinics.value = response.data;
  } catch (error) {
    console.error('Error fetching clinics:', error);
    showSnackbar('Erro ao carregar clínicas.', 'error');
  }
};

onMounted(() => {
  fetchPayers();
  fetchClinics();
});

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
    form.value?.resetValidation();
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
  if (!form.value) return;
  const { valid } = await form.value.validate();
  if (!valid) return;

  saveLoading.value = true;
  try {
    if (editedIndex.value > -1) {
      await apiClient.put(`/api/payers/${editedItem.value.id}/`, editedItem.value);
      showSnackbar('Convênio atualizado com sucesso!');
    } else {
      await apiClient.post('/api/payers/', editedItem.value);
      showSnackbar('Convênio criado com sucesso!');
    }
    fetchPayers();
  } catch (error) {
    console.error('Error saving payer:', error);
    showSnackbar('Erro ao salvar convênio.', 'error');
  } finally {
    saveLoading.value = false;
    close();
  }
};

const deleteItemConfirm = async () => {
  try {
    await apiClient.delete(`/api/payers/${editedItem.value.id}/`);
    showSnackbar('Convênio removido com sucesso!');
    fetchPayers();
  } catch (error) {
    console.error('Error deleting payer:', error);
    showSnackbar('Erro ao remover convênio.', 'error');
  } finally {
    closeDelete();
  }
};
</script>
