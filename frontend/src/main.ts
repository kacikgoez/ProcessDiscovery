import { createPinia } from 'pinia';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';

import App from './App.vue';
import './registerServiceWorker';

const routes = [
    { path: '/', component: App }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const pinia = createPinia()

createApp(App).
    use(router).
    use(pinia).
    use(PrimeVue).
    use(ConfirmationService).
    mount('#app')