import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import './assets/main.css';
import router from './router';
import 'remixicon/fonts/remixicon.css';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000'; // Your Django backend URL
axios.defaults.headers.common['Content-Type'] = 'application/json';

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

const app = createApp(App);
app.use(router);
app.use(pinia);
app.mount('#app');
