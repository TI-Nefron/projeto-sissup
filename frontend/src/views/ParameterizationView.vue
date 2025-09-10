<template>
  <v-container>
    <v-tabs v-model="tab" grow>
      <v-tab value="users">Usuários</v-tab>
      <v-tab value="clinics">Clínicas</v-tab>
      <v-tab value="guide-types">Tipos de Guia</v-tab>
      <v-tab value="procedure-statuses">Status de Procedimento</v-tab>
      <v-tab value="exit-types">Tipos de Saída</v-tab>
    </v-tabs>

    <v-window v-model="tab">
      <!-- Users Tab -->
      <v-window-item value="users">
        <v-card flat>
          <v-card-title class="d-flex align-center pe-2">
            <v-icon icon="mdi-account-group"></v-icon> &nbsp; Gerenciar Usuários
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="openUserDialog()">Novo Usuário</v-btn>
          </v-card-title>
          <v-data-table :headers="userHeaders" :items="users" :loading="loading">
            <template v-slot:item.roles="{ item }">
              <v-chip v-for="roleId in item.roles" :key="roleId" class="ma-1">
                {{ roleMap.get(roleId) }}
              </v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-icon class="me-2" size="small" @click="openUserDialog(item)">mdi-pencil</v-icon>
              <v-icon size="small" @click="deleteUser(item.id)">mdi-delete</v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-window-item>

      <!-- Clinics Tab -->
      <v-window-item value="clinics">
        <v-card flat>
          <v-card-title class="d-flex align-center pe-2">
            <v-icon icon="mdi-hospital-building"></v-icon> &nbsp; Gerenciar Clínicas
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="openClinicDialog()">Nova Clínica</v-btn>
          </v-card-title>
          <v-data-table :headers="clinicHeaders" :items="clinics" :loading="loading">
            <template v-slot:item.cnpj="{ value }">
              {{ formatCNPJ(value) }}
            </template>
            <template v-slot:item.actions="{ item }">
              <v-icon class="me-2" size="small" @click="openClinicDialog(item)">mdi-pencil</v-icon>
              <v-icon size="small" @click="deleteClinic(item.id)">mdi-delete</v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-window-item>

      <!-- Guide Types Tab -->
      <v-window-item value="guide-types">
        <v-card flat>
          <v-card-title class="d-flex align-center pe-2">
            <v-icon icon="mdi-file-document-outline"></v-icon> &nbsp; Gerenciar Tipos de Guia
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="openGuideTypeDialog()">Novo Tipo de Guia</v-btn>
          </v-card-title>
          <v-data-table :headers="guideTypeHeaders" :items="guideTypes" :loading="loading">
            <template v-slot:item.actions="{ item }">
              <v-icon class="me-2" size="small" @click="openGuideTypeDialog(item)">mdi-pencil</v-icon>
              <v-icon size="small" @click="deleteGuideType(item.id)">mdi-delete</v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-window-item>

      <!-- Procedure Statuses Tab -->
      <v-window-item value="procedure-statuses">
        <v-card flat>
          <v-card-title class="d-flex align-center pe-2">
            <v-icon icon="mdi-list-status"></v-icon> &nbsp; Gerenciar Status de Procedimento
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="openStatusDialog()">Novo Status</v-btn>
          </v-card-title>
          <v-data-table :headers="statusHeaders" :items="statuses" :loading="loading">
            <template v-slot:item.actions="{ item }">
              <v-icon class="me-2" size="small" @click="openStatusDialog(item)">mdi-pencil</v-icon>
              <v-icon size="small" @click="deleteStatus(item.id)">mdi-delete</v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-window-item>

      <!-- Exit Types Tab -->
      <v-window-item value="exit-types">
        <v-card flat>
          <v-card-title class="d-flex align-center pe-2">
            <v-icon icon="mdi-location-exit"></v-icon> &nbsp; Gerenciar Tipos de Saída
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="openExitTypeDialog()">Novo Tipo de Saída</v-btn>
          </v-card-title>
          <v-data-table :headers="exitTypeHeaders" :items="exitTypes" :loading="loading">
            <template v-slot:item.actions="{ item }">
              <v-icon class="me-2" size="small" @click="openExitTypeDialog(item)">mdi-pencil</v-icon>
              <v-icon size="small" @click="deleteExitType(item.id)">mdi-delete</v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-window-item>
    </v-window>

    <!-- User Dialog -->
    <v-dialog v-model="userDialog" max-width="600px">
      <v-card>
        <v-card-title><span class="text-h5">{{ editedUser.id ? 'Editar Usuário' : 'Novo Usuário' }}</span></v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6"><v-text-field v-model="editedUser.first_name" label="Nome"></v-text-field></v-col>
              <v-col cols="12" sm="6"><v-text-field v-model="editedUser.last_name" label="Sobrenome"></v-text-field></v-col>
              <v-col cols="12"><v-text-field v-model="editedUser.username" label="Usuário (Login)"></v-text-field></v-col>
              <v-col cols="12"><v-text-field v-model="editedUser.email" label="Email"></v-text-field></v-col>
              <v-col cols="12"><v-text-field v-model="editedUser.password" label="Senha" type="password" placeholder="Deixe em branco para não alterar"></v-text-field></v-col>
              <v-col cols="12"><v-select v-model="editedUser.clinics" :items="clinics" item-title="name" item-value="id" label="Clínicas" multiple chips></v-select></v-col>
              <v-col cols="12"><v-select v-model="editedUser.roles" :items="roles" item-title="name" item-value="id" label="Cargos" multiple chips></v-select></v-col>
              <v-col cols="12"><v-switch v-model="editedUser.is_superuser" label="Superusuário (acesso total)"></v-switch></v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeUserDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="saveUser">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Clinic Dialog -->
    <v-dialog v-model="clinicDialog" max-width="600px">
      <v-card>
        <v-card-title><span class="text-h5">{{ editedClinic.id ? 'Editar Clínica' : 'Nova Clínica' }}</span></v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12"><v-text-field v-model="editedClinic.name" label="Nome"></v-text-field></v-col>
              <v-col cols="12"><v-text-field v-model="editedClinic.cnpj" label="CNPJ" maxlength="18" :rules="[cnpjRule]"></v-text-field></v-col>
              <v-col cols="12"><v-switch v-model="editedClinic.is_active" label="Ativa"></v-switch></v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeClinicDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="saveClinic">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Guide Type Dialog -->
    <v-dialog v-model="guideTypeDialog" max-width="600px">
      <v-card>
        <v-card-title><span class="text-h5">{{ editedGuideType.id ? 'Editar Tipo de Guia' : 'Novo Tipo de Guia' }}</span></v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12"><v-text-field v-model="editedGuideType.name" label="Nome"></v-text-field></v-col>
              <v-col cols="12"><v-switch v-model="editedGuideType.is_active" label="Ativo"></v-switch></v-col>
              <v-col cols="12"><v-select v-model="editedGuideType.clinics" :items="clinics" item-title="name" item-value="id" label="Clínicas" multiple chips></v-select></v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeGuideTypeDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="saveGuideType">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Procedure Status Dialog -->
    <v-dialog v-model="statusDialog" max-width="600px">
      <v-card>
        <v-card-title><span class="text-h5">{{ editedStatus.id ? 'Editar Status' : 'Novo Status' }}</span></v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12"><v-text-field v-model="editedStatus.name" label="Nome"></v-text-field></v-col>
              <v-col cols="12"><v-text-field v-model="editedStatus.slug" label="Slug"></v-text-field></v-col>
              <v-col cols="12"><v-switch v-model="editedStatus.is_active" label="Ativo"></v-switch></v-col>
              <v-col cols="12"><v-select v-model="editedStatus.clinics" :items="clinics" item-title="name" item-value="id" label="Clínicas" multiple chips></v-select></v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeStatusDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="saveStatus">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Exit Type Dialog -->
    <v-dialog v-model="exitTypeDialog" max-width="600px">
      <v-card>
        <v-card-title><span class="text-h5">{{ editedExitType.id ? 'Editar Tipo de Saída' : 'Novo Tipo de Saída' }}</span></v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12"><v-text-field v-model="editedExitType.name" label="Nome"></v-text-field></v-col>
              <v-col cols="12"><v-text-field v-model="editedExitType.code" label="Código"></v-text-field></v-col>
              <v-col cols="12"><v-select v-model="editedExitType.clinics" :items="clinics" item-title="name" item-value="id" label="Clínicas" multiple chips></v-select></v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeExitTypeDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="saveExitType">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import * as adminApi from '@/services/administrationApi';
import type { Clinic } from '@/stores/clinic';
import type { GuideType, ProcedureStatus, ExitType, User, Role } from '@/services/administrationApi';

const tab = ref('users');
const loading = ref(false);
const roles = ref<Role[]>([]);

// --- General --- 
onMounted(() => {
  fetchUsers();
  fetchClinics();
  fetchGuideTypes();
  fetchStatuses();
  fetchExitTypes();
  fetchRoles();
});

async function fetchRoles() {
  try {
    const response = await adminApi.getRoles();
    roles.value = response.data;
    console.log('Roles:', response.data);
  } catch (e) {
    console.error(e);
  }
}

// --- Users --- 
const users = ref<User[]>([]);
const userDialog = ref(false);
const editedUser = ref<Partial<User>>({});
const roleMap = computed(() => {
  const map = new Map<string, string>();
  roles.value.forEach(role => map.set(role.id, role.name));
  return map;
});
const userHeaders = [
  { title: 'Usuário', key: 'username' },
  { title: 'Nome', key: 'first_name' },
  { title: 'Sobrenome', key: 'last_name' },
  { title: 'Email', key: 'email' },
  { title: 'Cargos', key: 'roles' },
  { title: 'Superusuário', key: 'is_superuser' },
  { title: 'Ações', key: 'actions', sortable: false },
];

async function fetchUsers() {
  loading.value = true;
  try { users.value = (await adminApi.getUsers()).data; } 
  catch (e) { console.error(e); } 
  finally { loading.value = false; }
}

function openUserDialog(item: User | null = null) {
  editedUser.value = item ? { ...item } : { username: '', first_name: '', last_name: '', email: '', is_superuser: false, clinics: [] };
  userDialog.value = true;
}

function closeUserDialog() { userDialog.value = false; }

async function saveUser() {
  const data = { ...editedUser.value };
  // Do not send an empty password
  if (data.password === '') {
    delete data.password;
  }
  if (data.id) {
    await adminApi.updateUser(data.id, data);
  } else {
    await adminApi.createUser(data);
  }
  closeUserDialog();
  await fetchUsers();
}

async function deleteUser(id: string) {
  if (!confirm('Tem certeza que deseja apagar este usuário?')) return;
  await adminApi.deleteUser(id);
  await fetchUsers();
}

// --- Clinics, GuideTypes, Statuses, ExitTypes logic... (is the same as before) ---
const clinics = ref<Clinic[]>([]);
const guideTypes = ref<GuideType[]>([]);
const statuses = ref<ProcedureStatus[]>([]);
const exitTypes = ref<ExitType[]>([]);
const clinicDialog = ref(false);
const guideTypeDialog = ref(false);
const statusDialog = ref(false);
const exitTypeDialog = ref(false);
const editedClinic = ref<Partial<Clinic>>({});
const editedGuideType = ref<Partial<GuideType>>({});
const editedStatus = ref<Partial<ProcedureStatus>>({});
const editedExitType = ref<Partial<ExitType>>({});

watch(() => editedClinic.value.name, (newValue, oldValue) => {
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
      editedClinic.value.name = formatted;
    }
  }
});

const cnpjRule = (v: string) => {
    if (!v) return true; // CNPJ is optional
    const cleaned = v.replace(/\D/g, '');
    if (cleaned.length !== 14 || /^(\d)\1{13}$/.test(cleaned)) {
        return 'CNPJ inválido';
    }
    let length = cleaned.length - 2;
    let numbers = cleaned.substring(0, length);
    const digits = cleaned.substring(length);
    let sum = 0;
    let pos = length - 7;
    for (let i = length; i >= 1; i--) {
        sum += parseInt(numbers.charAt(length - i)) * pos--;
        if (pos < 2) pos = 9;
    }
    let result = sum % 11 < 2 ? 0 : 11 - sum % 11;
    if (result !== parseInt(digits.charAt(0))) {
        return 'CNPJ inválido';
    }
    length = length + 1;
    numbers = cleaned.substring(0, length);
    sum = 0;
    pos = length - 7;
    for (let i = length; i >= 1; i--) {
        sum += parseInt(numbers.charAt(length - i)) * pos--;
        if (pos < 2) pos = 9;
    }
    result = sum % 11 < 2 ? 0 : 11 - sum % 11;
    if (result !== parseInt(digits.charAt(1))) {
        return 'CNPJ inválido';
    }
    return true;
};

watch(() => editedClinic.value.cnpj, (newValue, oldValue) => {
  if (newValue) {
    const cleaned = newValue.replace(/\D/g, '');
    let formatted = cleaned;
    if (cleaned.length > 2) {
      formatted = `${cleaned.slice(0, 2)}.${cleaned.slice(2)}`;
    }
    if (cleaned.length > 5) {
      formatted = `${formatted.slice(0, 6)}.${cleaned.slice(5)}`;
    }
    if (cleaned.length > 8) {
      formatted = `${formatted.slice(0, 10)}/${cleaned.slice(8)}`;
    }
    if (cleaned.length > 12) {
      formatted = `${formatted.slice(0, 15)}-${cleaned.slice(12)}`;
    }
    if (formatted !== newValue) {
        editedClinic.value.cnpj = formatted.slice(0, 18);
    }
  }
});

const formatCNPJ = (cnpj: string) => {
  if (!cnpj) return '';
  const cleaned = cnpj.replace(/\D/g, '');
  return cleaned.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
};
const clinicHeaders = [{ title: 'Nome', key: 'name' }, { title: 'CNPJ', key: 'cnpj' }, { title: 'Ativa', key: 'is_active' }, { title: 'Ações', key: 'actions', sortable: false }];
const guideTypeHeaders = [{ title: 'Nome', key: 'name' }, { title: 'Ativo', key: 'is_active' }, { title: 'Ações', key: 'actions', sortable: false }];
const statusHeaders = [{ title: 'Nome', key: 'name' }, { title: 'Slug', key: 'slug' }, { title: 'Ativo', key: 'is_active' }, { title: 'Ações', key: 'actions', sortable: false }];
const exitTypeHeaders = [{ title: 'Nome', key: 'name' }, { title: 'Código', key: 'code' }, { title: 'Ações', key: 'actions', sortable: false }];
async function fetchClinics() { try { const response = await adminApi.getClinics(); clinics.value = response.data; console.log('Clinics:', response.data); } catch (e) { console.error(e); } }
async function fetchGuideTypes() { try { const response = await adminApi.getGuideTypes(); guideTypes.value = response.data; console.log('Guide Types:', response.data); } catch (e) { console.error(e); } }
async function fetchStatuses() { try { const response = await adminApi.getProcedureStatuses(); statuses.value = response.data; console.log('Statuses:', response.data); } catch (e) { console.error(e); } }
async function fetchExitTypes() { try { const response = await adminApi.getExitTypes(); exitTypes.value = response.data; console.log('Exit Types:', response.data); } catch (e) { console.error(e); } }
function openClinicDialog(item: any) { editedClinic.value = item ? { ...item } : { name: '', cnpj: '', is_active: true }; clinicDialog.value = true; }
function closeClinicDialog() { clinicDialog.value = false; }
async function saveClinic() { 
  const dataToSave = { ...editedClinic.value };
  if (dataToSave.cnpj) {
    dataToSave.cnpj = dataToSave.cnpj.replace(/\D/g, '');
  }
  if (dataToSave.id) await adminApi.updateClinic(dataToSave.id, dataToSave); 
  else await adminApi.createClinic(dataToSave as any); 
  closeClinicDialog(); 
  await fetchClinics(); 
}
async function deleteClinic(id: string) { if (!confirm('Tem certeza?')) return; await adminApi.deleteClinic(id); await fetchClinics(); }
function openGuideTypeDialog(item: any) { editedGuideType.value = item ? { ...item } : { name: '', is_active: true, clinics: [] }; guideTypeDialog.value = true; }
function closeGuideTypeDialog() { guideTypeDialog.value = false; }
async function saveGuideType() { const d = editedGuideType.value; if (d.id) await adminApi.updateGuideType(d.id, d); else await adminApi.createGuideType(d as any); closeGuideTypeDialog(); await fetchGuideTypes(); }
async function deleteGuideType(id: string) { if (!confirm('Tem certeza?')) return; await adminApi.deleteGuideType(id); await fetchGuideTypes(); }
function openStatusDialog(item: any) { editedStatus.value = item ? { ...item } : { name: '', slug: '', is_active: true, clinics: [] }; statusDialog.value = true; }
function closeStatusDialog() { statusDialog.value = false; }
async function saveStatus() { const d = editedStatus.value; if (d.id) await adminApi.updateProcedureStatus(d.id, d); else await adminApi.createProcedureStatus(d as any); closeStatusDialog(); await fetchStatuses(); }
async function deleteStatus(id: string) { if (!confirm('Tem certeza?')) return; await adminApi.deleteProcedureStatus(id); await fetchStatuses(); }
function openExitTypeDialog(item: any) { editedExitType.value = item ? { ...item } : { name: '', code: '', clinics: [] }; exitTypeDialog.value = true; }
function closeExitTypeDialog() { exitTypeDialog.value = false; }
async function saveExitType() { const d = editedExitType.value; if (d.id) await adminApi.updateExitType(d.id, d); else await adminApi.createExitType(d as any); closeExitTypeDialog(); await fetchExitTypes(); }
async function deleteExitType(id: string) { if (!confirm('Tem certeza?')) return; await adminApi.deleteExitType(id); await fetchExitTypes(); }

</script>