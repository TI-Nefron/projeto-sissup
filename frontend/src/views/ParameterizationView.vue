<template>
  <v-container>
    <v-tabs v-model="tab" grow>
      <v-tab value="users">Usuários</v-tab>
      <v-tab value="clinics">Clínicas</v-tab>
      <v-tab value="document-types">Tipos de Documento</v-tab>
      <v-tab value="mandatory-docs">Documentos Obrigatórios</v-tab>
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

      <!-- Document Types Tab -->
      <v-window-item value="document-types">
        <v-card flat>
          <v-card-title class="d-flex align-center pe-2">
            <v-icon icon="mdi-file-document-multiple-outline"></v-icon> &nbsp; Gerenciar Tipos de Documento
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="openDocumentTypeDialog()">Novo Tipo</v-btn>
          </v-card-title>
          <v-data-table :headers="documentTypeHeaders" :items="documentTypes" :loading="loading">
            <template v-slot:item.category="{ value }">
              {{ value === 'PATIENT' ? 'Paciente' : 'Guia' }}
            </template>
            <template v-slot:item.actions="{ item }">
              <v-icon class="me-2" size="small" @click="openDocumentTypeDialog(item)">mdi-pencil</v-icon>
              <v-icon size="small" @click="deleteDocumentType(item.id)">mdi-delete</v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-window-item>

      <!-- Mandatory Docs Tab -->
      <v-window-item value="mandatory-docs">
        <v-card flat>
          <v-card-title>
            <v-icon icon="mdi-file-check-outline"></v-icon> &nbsp; Gerenciar Documentos Obrigatórios
          </v-card-title>
          <v-card-text>
            <v-select
              v-model="selectedClinicId"
              :items="clinics"
              item-title="name"
              item-value="id"
              label="Selecione uma Clínica"
              variant="outlined"
              class="mb-6"
            ></v-select>
            <div v-if="selectedClinicId">
              <v-row>
                <v-col cols="12" md="6">
                  <v-card-subtitle class="mb-2">Para Cadastro de Paciente</v-card-subtitle>
                  <v-list-item v-for="docType in patientDocTypes" :key="docType.id">
                    <v-checkbox
                      v-model="mandatoryDocIds"
                      :label="docType.name"
                      :value="docType.id"
                    ></v-checkbox>
                  </v-list-item>
                </v-col>
                <v-col cols="12" md="6">
                  <v-card-subtitle class="mb-2">Para Cadastro de Guia</v-card-subtitle>
                  <v-list-item v-for="docType in guideDocTypes" :key="docType.id">
                    <v-checkbox
                      v-model="mandatoryDocIds"
                      :label="docType.name"
                      :value="docType.id"
                    ></v-checkbox>
                  </v-list-item>
                </v-col>
              </v-row>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn 
                  color="primary"
                  :disabled="!hasMandatoryDocsChanged"
                  :loading="isSavingMandatoryDocs"
                  @click="updateMandatoryDocs"
                >
                  Salvar Alterações
                </v-btn>
              </v-card-actions>
            </div>
             <v-alert v-else type="info" text="Selecione uma clínica para começar."></v-alert>
          </v-card-text>
        </v-card>
      </v-window-item>

      <!-- Other tabs... -->
    </v-window>

    <!-- DIALOGS -->
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

    <v-dialog v-model="documentTypeDialog" max-width="600px">
      <v-card>
        <v-card-title><span class="text-h5">{{ editedDocumentType.id ? 'Editar Tipo de Documento' : 'Novo Tipo' }}</span></v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12"><v-text-field v-model="editedDocumentType.name" label="Nome"></v-text-field></v-col>
              <v-col cols="12">
                <v-select 
                  v-model="editedDocumentType.category" 
                  :items="[{title: 'Paciente', value: 'PATIENT'}, {title: 'Guia', value: 'GUIDE'}]" 
                  label="Categoria"
                ></v-select>
              </v-col>
              <v-col cols="12"><v-switch v-model="editedDocumentType.is_active" label="Ativo"></v-switch></v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeDocumentTypeDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="saveDocumentType">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import * as adminApi from '@/services/administrationApi';
import * as documentsApi from '@/services/documentsApi';
import type { DocumentType } from '@/services/documentsApi';
import type { Clinic } from '@/stores/clinic';
import type { GuideType, ProcedureStatus, ExitType, User, Role } from '@/services/administrationApi';
import { xor } from 'lodash-es';

// --- STATE ---
const tab = ref('users');
const loading = ref(false);

// Users state
const users = ref<User[]>([]);
const userDialog = ref(false);
const editedUser = ref<Partial<User>>({});
const roles = ref<Role[]>([]);
const roleMap = computed(() => new Map(roles.value.map(role => [role.id, role.name])));

// Clinics state
const clinics = ref<Clinic[]>([]);
const clinicDialog = ref(false);
const editedClinic = ref<Partial<Clinic>>({});

// Document Types state
const documentTypes = ref<DocumentType[]>([]);
const documentTypeDialog = ref(false);
const editedDocumentType = ref<Partial<DocumentType>>({});

// Mandatory Docs state
const selectedClinicId = ref<string | null>(null);
const mandatoryDocIds = ref<string[]>([]);
const originalMandatoryDocIds = ref<string[]>([]);
const isSavingMandatoryDocs = ref(false);

// Other parameterization states
const guideTypes = ref<GuideType[]>([]);
const statuses = ref<ProcedureStatus[]>([]);
const exitTypes = ref<ExitType[]>([]);
const guideTypeDialog = ref(false);
const statusDialog = ref(false);
const exitTypeDialog = ref(false);
const editedGuideType = ref<Partial<GuideType>>({});
const editedStatus = ref<Partial<ProcedureStatus>>({});
const editedExitType = ref<Partial<ExitType>>({});


// --- COMPUTED ---
const patientDocTypes = computed(() => documentTypes.value.filter(d => d.category === 'PATIENT'));
const guideDocTypes = computed(() => documentTypes.value.filter(d => d.category === 'GUIDE'));
const hasMandatoryDocsChanged = computed(() => {
  if (originalMandatoryDocIds.value.length !== mandatoryDocIds.value.length) return true;
  return xor(originalMandatoryDocIds.value, mandatoryDocIds.value).length > 0;
});


// --- HEADERS ---
const userHeaders = [ { title: 'Usuário', key: 'username' }, { title: 'Nome', key: 'first_name' }, { title: 'Sobrenome', key: 'last_name' }, { title: 'Email', key: 'email' }, { title: 'Cargos', key: 'roles' }, { title: 'Superusuário', key: 'is_superuser' }, { title: 'Ações', key: 'actions', sortable: false }, ];
const clinicHeaders = [{ title: 'Nome', key: 'name' }, { title: 'CNPJ', key: 'cnpj' }, { title: 'Ativa', key: 'is_active' }, { title: 'Ações', key: 'actions', sortable: false }];
const documentTypeHeaders = [ { title: 'Nome', key: 'name' }, { title: 'Categoria', key: 'category' }, { title: 'Ativo', key: 'is_active' }, { title: 'Ações', key: 'actions', sortable: false } ];
const guideTypeHeaders = [{ title: 'Nome', key: 'name' }, { title: 'Ativo', key: 'is_active' }, { title: 'Ações', key: 'actions', sortable: false }];
const statusHeaders = [{ title: 'Nome', key: 'name' }, { title: 'Slug', key: 'slug' }, { title: 'Ativo', key: 'is_active' }, { title: 'Ações', key: 'actions', sortable: false }];
const exitTypeHeaders = [{ title: 'Nome', key: 'name' }, { title: 'Código', key: 'code' }, { title: 'Ações', key: 'actions', sortable: false }];


// --- LIFECYCLE ---
onMounted(() => {
  fetchUsers();
  fetchClinics();
  fetchDocumentTypes();
  fetchGuideTypes();
  fetchStatuses();
  fetchExitTypes();
  fetchRoles();
});


// --- WATCHERS ---
watch(selectedClinicId, async (newClinicId) => {
  if (newClinicId) {
    try {
      loading.value = true;
      const response = await adminApi.getMandatoryDocuments(newClinicId);
      mandatoryDocIds.value = response.data;
      originalMandatoryDocIds.value = [...response.data];
    } catch (e) {
      console.error('Failed to fetch mandatory documents', e);
      mandatoryDocIds.value = [];
      originalMandatoryDocIds.value = [];
    } finally {
      loading.value = false;
    }
  }
});

watch(() => editedClinic.value.cnpj, (newValue) => {
  if (newValue) {
    const cleaned = newValue.replace(/\D/g, '');
    let formatted = cleaned;
    if (cleaned.length > 2) { formatted = `${cleaned.slice(0, 2)}.${cleaned.slice(2)}`; }
    if (cleaned.length > 5) { formatted = `${formatted.slice(0, 6)}.${cleaned.slice(5)}`; }
    if (cleaned.length > 8) { formatted = `${formatted.slice(0, 10)}/${cleaned.slice(8)}`; }
    if (cleaned.length > 12) { formatted = `${formatted.slice(0, 15)}-${cleaned.slice(12)}`; }
    if (formatted !== newValue) { editedClinic.value.cnpj = formatted.slice(0, 18); }
  }
});


// --- METHODS ---

// Document Types Methods
async function fetchDocumentTypes() {
  try {
    loading.value = true;
    documentTypes.value = (await documentsApi.getDocumentTypes()).data;
  } catch (e) { console.error(e); } finally { loading.value = false; }
}
function openDocumentTypeDialog(item: DocumentType | null = null) {
  editedDocumentType.value = item ? { ...item } : { name: '', category: 'PATIENT', is_active: true };
  documentTypeDialog.value = true;
}
function closeDocumentTypeDialog() { documentTypeDialog.value = false; }
async function saveDocumentType() {
  const data = editedDocumentType.value;
  if (data.id) {
    await documentsApi.updateDocumentType(data.id, data);
  } else {
    await documentsApi.createDocumentType(data as DocumentType);
  }
  closeDocumentTypeDialog();
  await fetchDocumentTypes();
}
async function deleteDocumentType(id: string) {
  if (!confirm('Tem certeza? Apagar um tipo de documento pode afetar configurações existentes.')) return;
  await documentsApi.deleteDocumentType(id);
  await fetchDocumentTypes();
}

// Mandatory Docs Methods
async function updateMandatoryDocs() {
  if (selectedClinicId.value) {
    isSavingMandatoryDocs.value = true;
    try {
      await adminApi.setMandatoryDocuments(selectedClinicId.value, mandatoryDocIds.value);
      originalMandatoryDocIds.value = [...mandatoryDocIds.value];
    } catch (e) {
      console.error('Failed to update mandatory documents', e);
    } finally {
      isSavingMandatoryDocs.value = false;
    }
  }
}

// Users Methods
async function fetchUsers() { try { loading.value = true; users.value = (await adminApi.getUsers()).data; } catch (e) { console.error(e); } finally { loading.value = false; } }
function openUserDialog(item: User | null = null) { editedUser.value = item ? { ...item } : { username: '', first_name: '', last_name: '', email: '', is_superuser: false, clinics: [], roles: [] }; userDialog.value = true; }
function closeUserDialog() { userDialog.value = false; }
async function saveUser() { const data = { ...editedUser.value }; if (data.password === '') { delete data.password; } if (data.id) { await adminApi.updateUser(data.id, data); } else { await adminApi.createUser(data); } closeUserDialog(); await fetchUsers(); }
async function deleteUser(id: string) { if (!confirm('Tem certeza?')) return; await adminApi.deleteUser(id); await fetchUsers(); }
async function fetchRoles() { try { roles.value = (await adminApi.getRoles()).data; } catch (e) { console.error(e); } }

// Clinics Methods
async function fetchClinics() { try { clinics.value = (await adminApi.getClinics()).data; } catch (e) { console.error(e); } }
function openClinicDialog(item: any) { editedClinic.value = item ? { ...item } : { name: '', cnpj: '', is_active: true }; clinicDialog.value = true; }
function closeClinicDialog() { clinicDialog.value = false; }
async function saveClinic() { const dataToSave = { ...editedClinic.value }; if (dataToSave.cnpj) { dataToSave.cnpj = dataToSave.cnpj.replace(/\D/g, ''); } if (dataToSave.id) await adminApi.updateClinic(dataToSave.id, dataToSave); else await adminApi.createClinic(dataToSave as any); closeClinicDialog(); await fetchClinics(); }
async function deleteClinic(id: string) { if (!confirm('Tem certeza?')) return; await adminApi.deleteClinic(id); await fetchClinics(); }
const cnpjRule = (v: string) => {
    if (!v) return true;
    const cleaned = v.replace(/\D/g, '');
    if (cleaned.length !== 14 || /^(\d)\1{13}$/.test(cleaned)) { return 'CNPJ inválido'; }
    let length = cleaned.length - 2;
    let numbers = cleaned.substring(0, length);
    const digits = cleaned.substring(length);
    let sum = 0;
    let pos = length - 7;
    for (let i = length; i >= 1; i--) { sum += parseInt(numbers.charAt(length - i)) * pos--; if (pos < 2) pos = 9; }
    let result = sum % 11 < 2 ? 0 : 11 - sum % 11;
    if (result !== parseInt(digits.charAt(0))) { return 'CNPJ inválido'; }
    length = length + 1;
    numbers = cleaned.substring(0, length);
    sum = 0;
    pos = length - 7;
    for (let i = length; i >= 1; i--) { sum += parseInt(numbers.charAt(length - i)) * pos--; if (pos < 2) pos = 9; }
    result = sum % 11 < 2 ? 0 : 11 - sum % 11;
    if (result !== parseInt(digits.charAt(1))) { return 'CNPJ inválido'; }
    return true;
};
const formatCNPJ = (cnpj: string) => { if (!cnpj) return ''; const cleaned = cnpj.replace(/\D/g, ''); return cleaned.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5'); };

// Other Parameterization Methods
async function fetchGuideTypes() { try { guideTypes.value = (await adminApi.getGuideTypes()).data; } catch (e) { console.error(e); } }
async function fetchStatuses() { try { statuses.value = (await adminApi.getProcedureStatuses()).data; } catch (e) { console.error(e); } }
async function fetchExitTypes() { try { exitTypes.value = (await adminApi.getExitTypes()).data; } catch (e) { console.error(e); } }
const openGuideTypeDialog = (item: any) => {};
const deleteGuideType = (id: string) => {};
const openStatusDialog = (item: any) => {};
const deleteStatus = (id: string) => {};
const openExitTypeDialog = (item: any) => {};
const deleteExitType = (id: string) => {};

</script>
