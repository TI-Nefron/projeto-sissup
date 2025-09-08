
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import apiClient from '@/services/api';
import { useUserStore } from './user';

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false);
  const userStore = useUserStore();

  const login = async (credentials: any) => {
    try {
      const response = await apiClient.post('/api-auth/login/', credentials, {
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
          }
      });
      // A successful login does not have non_field_errors.
      if (response.data && response.data.non_field_errors) {
        throw new Error('Login failed due to credentials.');
      }
      isAuthenticated.value = true;
      await userStore.fetchUser();
    } catch (error) {
      isAuthenticated.value = false;
      userStore.clearUser();
      throw error; // Re-throw the error to be caught by the view
    }
  };

  const logout = async () => {
    await apiClient.post('/api-auth/logout/');
    isAuthenticated.value = false;
    userStore.clearUser();
  };

  const checkAuth = async () => {
    try {
      // If there's no user data, try fetching it.
      if (!userStore.user) {
        await userStore.fetchUser();
      }
      isAuthenticated.value = !!userStore.user;
    } catch (error) {
      isAuthenticated.value = false;
      userStore.clearUser();
    }
  };

  return { isAuthenticated, login, logout, checkAuth };
});
