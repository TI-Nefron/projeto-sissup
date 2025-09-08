
import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '@/services/api';

export const useUserStore = defineStore('user', () => {
  const user = ref(null);

  const fetchUser = async () => {
    const response = await apiClient.get('/api/user/');
    user.value = response.data;
  };

  const clearUser = () => {
    user.value = null;
  };

  return { user, fetchUser, clearUser };
});
