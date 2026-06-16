<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import { ref } from 'vue';
import BaseButton from '@/components/BaseButton.vue';


const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const isMenuOpen = ref(false);

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value;
};

const closeMenu = () => {
    isMenuOpen.value = false;
};

const handleLogout = () => {
    authStore.logout();
    closeMenu();
    router.push('/login');
}
</script>

<template>
    <nav>
        <!-- Ligne du haut : logo + hamburger (mobile) / logo + liens (desktop) -->
        <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">

            <!-- Logo -->
            <template v-if="route.name !=='profile' && route.name !=='register' && route.name !=='login'">
                <router-link to="/rolls" class="flex items-center gap-3">
                    <img 
                        src="@/assets/logo/logo2.png" 
                        alt="One Roll" 
                        class="h-20 md:h-24 w-auto"
                    />
                    
                </router-link>
            </template> 
            <div v-else></div>

            <!-- Bouton hamburger -> visible seulement sur mobile -->
            <button class="md:hidden text-3xl text-film px-2 py-1" @click="toggleMenu">
                ☰
            </button>

            <!-- Menu horizontal desktop -> caché sur mobile-->
            <div class="hidden md:flex flex-col items-end gap-4">
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

                        <router-link to="/dashboard" class="hover:text-amber" active-class="text-amber font-semibold">
                            Tableau de bord
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

            <!-- Menu déroulant mobile -> caché sur desktop -->
            <div v-show="isMenuOpen" class="md:hidden flex flex-col items-center gap-4 absolute top-20 right-4 bg-white p-4 rounded shadow-lg z-50">
                <template v-if="authStore.user">
                    <router-link to="/rolls" class="hover:text-amber" active-class="text-amber font-semibold" @click="closeMenu">
                        Films
                    </router-link>

                    <router-link to="/cameras" class="hover:text-amber" active-class="text-amber font-semibold" @click="closeMenu">
                        Appareils   
                    </router-link>

                    <router-link to="/profile" class="hover:text-amber" active-class="text-amber font-semibold" @click="closeMenu">
                        Profil   
                    </router-link>

                    <router-link to="/dashboard" class="hover:text-amber" active-class="text-amber font-semibold" @click="closeMenu">
                        Tableau de bord
                    </router-link>

                    <button
                        @click="handleLogout"
                        class="hover:text-danger"
                        >
                            Déconnexion
                    </button>

                    <BaseButton to="/rolls/new" size="sm" @click="closeMenu">
                        + Pellicule
                    </BaseButton>

                    <BaseButton to="/cameras/new" size="sm" @click="closeMenu">
                        + Appareil
                    </BaseButton>

                    <BaseButton to="/lenses/new" size="sm" @click="closeMenu">
                        + Objectif
                    </BaseButton>
                </template>
                <template v-else>
                    <router-link to="/login" class="hover:text-amber" @click="closeMenu">
                        Connexion
                    </router-link>

                    <router-link to="/register" class="hover:text-amber" @click="closeMenu">
                        Inscription   
                    </router-link>

                </template>
            </div> 
        </div>
    </nav>
</template>