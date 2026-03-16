import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAuthStore } from './stores/auth'

import App from './App.vue'
import router from './router'

const authStore = useAuthStore()

if (authStore.accessToken) {
    authStore.fetchUser()
}

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
