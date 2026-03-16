<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRoute } from 'vue-router';

const authStore = useAuthStore();
const router = useRoute();

const handleLogout = () => {
    authStore.logout();
    router.push('/login');
}
</script>

<template>
    <nav class="navbar">
        <div class="links">

            <template v-if="authStore.user">
                <router-link to="/rolls">Pellicules</router-link>
                <router-link to="/cameras">Appareils photo</router-link>
                <router-link to="/lenses">Objectifs</router-link>

                <button @click="handleLogout">Déconnexion</button>
            </template>

            <template v-else>
                <router-link to="/login">Connexion</router-link>
                <router-link to="/register">Inscription</router-link>
            </template>

            <button @click="handleLogout">Déconnexion</button>

        </div>
    </nav>
</template>