import { createRouter, createWebHistory } from 'vue-router';
import PatientListView from '../views/PatientListView.vue';
import GuideListView from '../views/GuideListView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/patients',
    },
    {
      path: '/patients',
      name: 'patients',
      component: PatientListView,
    },
    {
      path: '/guides',
      name: 'guides',
      component: GuideListView,
    },
  ],
});

export default router;
