<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
    authStore.logout();
    router.push('/login');
}
</script>

<template>
    <nav class="bg-paper border-b border-gray-200">
        <div class="maw-w-6xl mx-auto px-4 py-3 flex items-center justify-between">

            <!-- Logo -->
            <router-link to="/rolls" class="flex items-ceter gap-3">
                <img 
                    src="@/assets/logo/logo2.png" 
                    alt="One Roll" 
                    class="h-24 w-auto"
                />
                <!-- <div class="hidden sm:block">
                    <p class="font-title text-sm text-film leading-tight">
                        ONE ROLL
                    </p>
                    <p class="text-[10px] text-grain">
                        TO RUL THEM ALL
                    </p>
                </div> -->
            </router-link>

            <!-- Navigation Links -->
            <div class="flex items-center gap-6 text-sm font-ui text-film">
                <template v-if="authStore.user">
                    <router-link to="/rolls" class="hover:text-amber">
                        Films
                    </router-link>

                    <router-link to="/cameras" class="hover:text-amber">
                        Appareils   
                    </router-link>

                    <router-link to="/profile" class="hover:text-amber">
                        Profil   
                    </router-link>

                    <button
                        @click="handleLogout"
                        class="hover:text-danger"
                    >
                        Déconnexion
                    </button>
                </template>

                <template v-else>
                    <router-link to="/login" class="hover:text-amber">
                        Connexion
                    </router-link>

                    <router-link to="/register" class="hover:text-amber">
                        Inscription   
                    </router-link>
                </template>

            </div>
        </div>
    </nav>
</template>