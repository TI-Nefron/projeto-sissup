import { createRouter, createWebHistory } from 'vue-router';
import PatientListView from '../views/PatientListView.vue';
import GuideListView from '../views/GuideListView.vue';
import PatientFormView from '../views/PatientFormView.vue';
import GuideFormView from '../views/GuideFormView.vue';
import LoginView from '../views/LoginView.vue';
import LobbyView from '../views/LobbyView.vue';
import PayerListView from '../views/PayerListView.vue';
import PatientHistoryView from '../views/PatientHistoryView.vue';
import ClinicSelectionView from '../views/ClinicSelectionView.vue';
import ParameterizationView from '../views/ParameterizationView.vue';
import AuditLogView from '../views/AuditLogView.vue';
import { useAuthStore } from '@/stores/auth';
import { useClinicStore } from '@/stores/clinic';

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
      path: '/clinic-selection',
      name: 'clinic-selection',
      component: ClinicSelectionView,
      meta: { requiresAuth: true },
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
      path: '/guides/new',
      name: 'new-guide',
      component: GuideFormView,
      meta: { requiresAuth: true },
    },
    {
      path: '/guides/:id/edit',
      name: 'edit-guide',
      component: GuideFormView,
      meta: { requiresAuth: true },
    },
    {
      path: '/payers',
      name: 'payers',
      component: PayerListView,
      meta: { requiresAuth: true },
    },
    {
      path: '/history',
      name: 'history',
      component: PatientHistoryView,
      meta: { requiresAuth: true },
    },
    {
      path: '/parameterization',
      name: 'parameterization',
      component: ParameterizationView,
      meta: { requiresAuth: true, requiresSuperuser: true },
    },
    {
      path: '/audit-logs',
      name: 'audit-logs',
      component: AuditLogView,
      meta: { requiresAuth: true, requiresSuperuser: true },
    },
  ],
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  const clinicStore = useClinicStore();
  const requiresAuth = to.meta.requiresAuth;
  const requiresSuperuser = to.meta.requiresSuperuser;

  // This will also fetch the user data if not present
  await authStore.checkAuth();

  const isAuthenticated = authStore.isAuthenticated;
  const isSuperuser = authStore.user?.is_superuser;

  if (requiresAuth && !isAuthenticated) {
    // 1. If route requires auth and user is not logged in, clear any lingering
    // clinic selection and redirect to login.
    clinicStore.clearClinic();
    return next({ name: 'login' });
  }

  if (requiresSuperuser && !isSuperuser) {
    // If route requires superuser and user is not one, redirect to lobby.
    return next({ name: 'lobby' });
  }

  if (isAuthenticated && to.name === 'login') {
    // 2. If user is logged in and tries to go to login, redirect to lobby.
    return next({ name: 'lobby' });
  }

  if (isAuthenticated && requiresAuth && !clinicStore.selectedClinic && to.name !== 'clinic-selection' && to.name !== 'parameterization') {
    // 3. If user is logged in but has not selected a clinic, force them to the selection screen.
    return next({ name: 'clinic-selection' });
  }

  if (isAuthenticated && clinicStore.selectedClinic && to.name === 'clinic-selection') {
    // 4. If user has a clinic selected and tries to go to the selection screen, redirect to lobby.
    return next({ name: 'lobby' });
  }

  // Otherwise, allow navigation.
  next();
});

export default router;
