
<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Usuário"
                name="username"
                prepend-icon="mdi-account"
                type="text"
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Senha"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
              ></v-text-field>
              <v-alert v-if="error" type="error" dense>
                {{ error }}
              </v-alert>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn type="submit" color="primary">Entrar</v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const username = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();
const authStore = useAuthStore();

const handleLogin = async () => {
  error.value = ''; // Clear previous errors
  try {
    const params = new URLSearchParams();
    params.append('username', username.value);
    params.append('password', password.value);

    await authStore.login(params);

    // After successful login, the navigation guard will automatically redirect
    // to '/patients' if the user is still on '/login'.
    await router.push('/lobby');

  } catch (err: any) {
    error.value = 'Usuário ou senha inválidos.';
    console.error('Login error:', err);
  }
};
</script>
