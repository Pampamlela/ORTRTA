<script setup>
import { useAuthStore } from './stores/auth'
import { onMounted } from 'vue';
import Navbar from './components/Navbar.vue';

const authStore = useAuthStore()

onMounted(() => {
    if (authStore.accessToken) {
        authStore.fetchUser()
    }
})
</script>

<template>

  <Navbar />

  <router-view />
  
</template>
