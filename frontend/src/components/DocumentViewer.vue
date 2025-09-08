<template>
  <v-dialog v-model="dialog" fullscreen>
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="dialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Visualizador de Documentos</v-toolbar-title>
      </v-toolbar>
      <v-row no-gutters>
        <v-col cols="6">
          <iframe :src="doc1url" width="100%" height="100%"></iframe>
        </v-col>
        <v-col cols="6">
          <iframe :src="doc2url" width="100%" height="100%"></iframe>
        </v-col>
      </v-row>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, defineProps, watch, defineEmits } from 'vue';

const props = defineProps({
  modelValue: Boolean,
  doc1url: String,
  doc2url: String,
});

const emit = defineEmits(['update:modelValue']);

const dialog = ref(props.modelValue);

watch(() => props.modelValue, (val) => {
  dialog.value = val;
});

watch(dialog, (val) => {
  if (!val) {
    emit('update:modelValue', false);
  }
});
</script>

<style scoped>
iframe {
  border: none;
  height: calc(100vh - 64px); /* 64px is the toolbar height */
}
</style>
