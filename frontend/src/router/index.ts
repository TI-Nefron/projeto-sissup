import { createRouter, createWebHistory } from 'vue-router';
import PatientListView from '../views/PatientListView.vue';
import GuideListView from '../views/GuideListView.vue';
import PatientFormView from '../views/PatientFormView.vue';
import LoginView from '../views/LoginView.vue';
import LobbyView from '../views/LobbyView.vue';
import ClinicListView from '../views/ClinicListView.vue';
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/lobby', // Redirect root to lobby
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/lobby',
      name: 'lobby',
      component: LobbyView,
      meta: { requiresAuth: true },
    },
    {
      path: '/patients',
      name: 'patients',
      component: PatientListView,
      meta: { requiresAuth: true },
    },
    {
      path: '/patients/new',
      name: 'new-patient',
      component: PatientFormView,
      meta: { requiresAuth: true },
    },
    {
      path: '/patients/:id/edit',
      name: 'edit-patient',
      component: PatientFormView,
      meta: { requiresAuth: true },
    },
    {
      path: '/guides',
      name: 'guides',
      component: GuideListView,
      meta: { requiresAuth: true },
    },
    {
      path: '/clinics',
      name: 'clinics',
      component: ClinicListView,
      meta: { requiresAuth: true },
    },
    {
      path: '/payers',
      name: 'payers',
      component: PayerListView,
      meta: { requiresAuth: true },
    },
  ],
});

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();
  const requiresAuth = to.meta.requiresAuth;

  // Ensure we have checked for an existing session
  await auth.checkAuth();

  if (requiresAuth && !auth.isAuthenticated) {
    // If the route requires auth and the user is not authenticated, redirect to login.
    next({ name: 'login' });
  } else if (to.name === 'login' && auth.isAuthenticated) {
    // If the user is authenticated and tries to access the login page, redirect them to the lobby.
    next({ name: 'lobby' });
  } else {
    // Otherwise, allow the navigation.
    next();
  }
});

export default router;
