<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import BaseButton from '@/components/BaseButton.vue';


const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const handleLogout = () => {
    authStore.logout();
    router.push('/login');
}
</script>

<template>
    <nav>
        <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">

            <!-- Logo -->
            <template v-if="route.name !=='profile' && route.name !=='register' && route.name !=='login'">
                <router-link to="/rolls" class="flex items-center gap-3">
                    <img 
                        src="@/assets/logo/logo2.png" 
                        alt="One Roll" 
                        class="h-16 md:h-24 w-auto"
                    />
                    
                </router-link>
            </template> 
            <div v-else></div>

            <!-- Navigation Links -->
            <div class="flex flex-col items-end gap-6 text-sm font-ui text-film">
                <template v-if="authStore.user">

                    <!-- ligne 1 : les liens -->
                    <div class="flex items-center gap-6">
                        <router-link to="/rolls" class="hover:text-amber" active-class="text-amber font-semibold">
                            Films
                        </router-link>

                        <router-link to="/cameras" class="hover:text-amber" active-class="text-amber font-semibold">
                            Appareils   
                        </router-link>

                        <router-link to="/profile" class="hover:text-amber" active-class="text-amber font-semibold">
                            Profil   
                        </router-link>

                        <button
                            @click="handleLogout"
                            class="hover:text-danger"
                        >
                            Déconnexion
                        </button>
                    </div>

                    <!-- ligne 2 : les boutons -->
                    <div class="flex gap-3">
                        <BaseButton to="/rolls/new" size="sm">
                            + Pellicule
                        </BaseButton>

                        <BaseButton to="/cameras/new" size="sm">
                            + Appareil
                        </BaseButton>

                        <BaseButton to="/lenses/new" size="sm">
                            + Objectif
                        </BaseButton>
                    </div>
                </template>

                <template v-else>
                    <div class="flex items-center gap-6">
                        <router-link to="/login" class="hover:text-amber">
                            Connexion
                        </router-link>

                        <router-link to="/register" class="hover:text-amber">
                            Inscription   
                        </router-link>
                    </div>
                </template>

            </div>
        </div>
    </nav>
</template>