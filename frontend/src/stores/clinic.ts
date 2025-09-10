import { defineStore } from 'pinia';
import { ref, watch } from 'vue';

// Tenta carregar a clínica do localStorage ao iniciar
const initialClinic = localStorage.getItem('selectedClinic');

export const useClinicStore = defineStore('clinic', () => {
  // O estado inicial é o que foi encontrado no localStorage ou null
  const selectedClinic = ref<any>(initialClinic ? JSON.parse(initialClinic) : null);

  // Ação para definir a clínica selecionada
  function selectClinic(clinic: any) {
    selectedClinic.value = clinic;
  }

  // Ação para limpar a clínica (ex: no logout)
  function clearClinic() {
    selectedClinic.value = null;
  }

  // Observa mudanças na clínica selecionada e persiste no localStorage
  watch(selectedClinic, (newClinic) => {
    if (newClinic) {
      localStorage.setItem('selectedClinic', JSON.stringify(newClinic));
    } else {
      localStorage.removeItem('selectedClinic');
    }
  }, { deep: true });

  return { selectedClinic, selectClinic, clearClinic };
});
