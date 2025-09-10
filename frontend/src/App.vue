<template>
  <v-app>
    <v-navigation-drawer v-if="showMenu" v-model="drawer" app>
      <v-list>
        <v-list-item prepend-icon="mdi-home" title="Início" to="/lobby"></v-list-item>
        <v-list-item prepend-icon="mdi-account-group" title="Pacientes" to="/patients"></v-list-item>
        <v-list-item prepend-icon="mdi-file-document-multiple" title="Guias" to="/guides"></v-list-item>
        <v-list-item prepend-icon="mdi-history" title="Histórico" to="/history"></v-list-item>
        <v-list-item to="/payers" title="Convênios" prepend-icon="mdi-card-account-details-outline"></v-list-item>
        <v-list-item v-if="authStore.user?.is_superuser" to="/audit-logs" title="Logs de Auditoria" prepend-icon="mdi-shield-lock"></v-list-item>
      </v-list>
    </v-navigation-drawer>

        <v-app-bar app color="primary">
      <v-app-bar-nav-icon v-if="showMenu" @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>GrupoNefron SISSUP <span v-if="clinicStore.selectedClinic">- {{ clinicStore.selectedClinic.name }}</span></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="route.name === 'parameterization'" to="/clinic-selection" prepend-icon="mdi-arrow-left" class="mr-2">Voltar à Seleção</v-btn>
      <v-btn v-if="authStore.user?.is_superuser && route.name === 'clinic-selection'" to="/parameterization" prepend-icon="mdi-cogs" class="mr-2">Parametrização</v-btn>
      <v-btn v-if="showMenu" @click="changeClinic" class="mr-2">Trocar Clínica</v-btn>
      <v-btn v-if="authStore.isAuthenticated" @click="logout">Sair</v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth';
import { useClinicStore } from '@/stores/clinic';
import { useRouter, useRoute } from 'vue-router';

const drawer = ref(false)
const authStore = useAuthStore();
const clinicStore = useClinicStore();
const router = useRouter();
const route = useRoute();

const showMenu = computed(() => {
  if (!authStore.isAuthenticated) return false;
  const nonMenuRoutes = ['clinic-selection', 'parameterization'];
  return !nonMenuRoutes.includes(route.name as string);
});

const logout = async () => {
  await authStore.logout();
  router.push('/login');
};

const changeClinic = () => {
  clinicStore.clearClinic();
  router.push('/clinic-selection');
};
</script>

<style>
/* Global styles can go here */
</style>