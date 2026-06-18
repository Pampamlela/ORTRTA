<script setup>
import { useAuthStore } from './stores/auth'
import { onMounted } from 'vue';
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
import { apiError } from './api/axios';
import ToastNotification from './components/ToastNotification.vue';

const authStore = useAuthStore()

const closeError = () => {
    apiError.value = null
}

onMounted(() => {
    if (authStore.accessToken) {
        authStore.fetchUser()
    }
})
</script>

<template>
    <div class="min-h-screen flex flex-col bg-paper">
        <Navbar />
        <ToastNotification />

        <!--Bandeau d'erreur-->
        <div v-if="apiError" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3">
            {{ apiError }}
            <button @click="closeError" class="ml-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                X
            </button>
        </div>

        <main class="flex-1">
            <router-view />
        </main>

        <Footer />

    </div>
</template>
