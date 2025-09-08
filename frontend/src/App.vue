<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item prepend-icon="mdi-account-group" title="Pacientes" to="/patients"></v-list-item>
        <v-list-item prepend-icon="mdi-file-document-multiple" title="Guias" to="/guides"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="primary">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>GrupoNefron SISSUP</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const drawer = ref(true)
</script>

<style>
/* Global styles can go here */
</style>
