<template>
  <v-container>
    <v-row justify="center" class="mt-8">
      <v-col cols="12" class="text-center">
        <h1 class="text-h4">Bem-vindo ao SISSUP</h1>
        <p class="text-subtitle-1 mt-2">Selecione um módulo para começar</p>
      </v-col>
    </v-row>

    <v-row class="mt-8" justify="center">
      <v-col cols="12" md="4" sm="6">
        <v-card
          class="mx-auto"
          max-width="344"
          hover
          to="/patients"
        >
          <v-card-item class="text-center">
            <v-icon size="64" class="my-4">mdi-account-group</v-icon>
            <v-card-title class="text-h5">
              Pacientes
            </v-card-title>
          </v-card-item>

          <v-card-text class="text-center">
            Gestão completa do cadastro de pacientes, incluindo informações pessoais, de tratamento e status.
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4" sm="6">
        <v-card
          class="mx-auto"
          max-width="344"
          hover
          to="/guides"
        >
          <v-card-item class="text-center">
            <v-icon size="64" class="my-4">mdi-file-document-multiple</v-icon>
            <v-card-title class="text-h5">
              Guias
            </v-card-title>
          </v-card-item>

          <v-card-text class="text-center">
            Controle e auditoria das guias de faturamento, com filtros avançados e visualização de documentos.
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
// No script needed for this simple view
</script>

<style scoped>
.v-card {
  transition: all 0.2s ease-in-out;
}
.v-card:hover {
  transform: scale(1.05);
}
</style>
