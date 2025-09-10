<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Bem-vindo, {{ userStore.user?.first_name }}!</v-toolbar-title>
          </v-toolbar>
          <v-card-text class="text-center">
            <h2 class="text-h6 pa-4">Selecione uma clínica para continuar</h2>
            <v-chip
              v-for="clinic in userStore.user?.clinics"
              :key="clinic.id"
              class="ma-2"
              color="primary"
              variant="elevated"
              size="large"
              @click="handleClinicSelection(clinic)"
            >
              <v-icon start icon="mdi-hospital-building"></v-icon>
              {{ clinic.name }}
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useClinicStore } from '@/stores/clinic';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const userStore = useUserStore();
const clinicStore = useClinicStore();
const authStore = useAuthStore();

const handleClinicSelection = (clinic: any) => {
  clinicStore.selectClinic(clinic);
  router.push('/lobby');
};
</script>

<style scoped>
.v-chip {
  cursor: pointer;
  transition: transform 0.2s;
}

.v-chip:hover {
  transform: scale(1.05);
}
</style>
