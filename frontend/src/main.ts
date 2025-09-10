import './assets/main.css';
import './styles/typography.css';
import '@mdi/font/css/materialdesignicons.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';

// Vuetify
import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import { pt } from 'vuetify/locale';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { GrupoNefronTheme } from './theme';

const vuetify = createVuetify({
  components,
  directives,
  locale: {
    locale: 'pt',
    fallback: 'pt',
    messages: { pt },
  },
  theme: {
    defaultTheme: 'GrupoNefronTheme',
    themes: {
      GrupoNefronTheme,
    },
  },
  icons: {
    defaultSet: 'mdi',
  },
});

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(vuetify);

app.mount('#app');
