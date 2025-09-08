<template>
  <v-app>
    <v-navigation-drawer v-if="authStore.isAuthenticated" v-model="drawer" app>
      <v-list>
        <v-list-item prepend-icon="mdi-home" title="Lobby" to="/lobby" @click="drawer = false"></v-list-item>
        <v-list-item prepend-icon="mdi-account-group" title="Pacientes" to="/patients" @click="drawer = false"></v-list-item>
        <v-list-item prepend-icon="mdi-file-document-multiple" title="Guias" to="/guides" @click="drawer = false"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="primary">
      <v-app-bar-nav-icon v-if="authStore.isAuthenticated" @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>GrupoNefron SISSUP</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-menu v-if="authStore.isAuthenticated" location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props">
            Cadastros
            <v-icon end>mdi-menu-down</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item to="/clinics" link>
            <v-list-item-title>Clínicas</v-list-item-title>
          </v-list-item>
          <v-list-item to="/payers" link>
            <v-list-item-title>Convênios</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

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
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const drawer = ref(false)
const authStore = useAuthStore();
const router = useRouter();

const logout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<style>
/* Global styles can go here */
</style>