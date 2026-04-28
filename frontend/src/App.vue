<script setup>
import { useAuthStore } from './stores/auth'
import { onMounted } from 'vue';
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';

const authStore = useAuthStore()

onMounted(() => {
    if (authStore.accessToken) {
        authStore.fetchUser()
    }
})
</script>

<template>
    <div class="min-h-screen flex flex-col bg-paper">
        <Navbar />

        <main class="flex-1">
            <router-view />
        </main>

        <Footer />

    </div>
</template>
