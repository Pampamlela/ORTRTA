<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import BaseButton from '@/components/BaseButton.vue';

const authStore = useAuthStore();
const router = useRouter();

const form = ref({
    email: '',
    password: '',
    password2: '',
});

const error = ref(null);

const handleResetPassword = async () => {
    try {
        await authStore.resetPassword(form.value);
        router.push('/login');
    } catch {
        error.value = 'Erreur lors de la réinitialisation du mot de passe';
    }
};
</script>

<template>
    <div class="px-4 py-6 max-w-5xl mx-auto flex flex-col md:grid md:grid-cols-2 md:gap-12 items-center"> 
        <!-- Colonne gauche : logo -->
        <div class="hidden md:flex justify-center items-center">
            <img
            src="@/assets/logo/logo2.png" 
            alt="One Roll"
            class="h-auto w-auto"
            />
        </div>

        <!-- Mobile : logo au-dessus du formulaire -->
        <div class="flex justify-center md:hidden mb-4">
            <img
            src="@/assets/logo/logo2.png" 
            alt="One Roll"
            class="h-48 w-auto"
            />
        </div>

        <!-- Colonne droite : contenu -->
        <div>
            <h1 class="font-title text-2xl md:text-3xl mb-6 text-film">Réinitialiser le mot de passe</h1>
            <h2 class="font-title text-sm md:text-xl mb-6 text-grain">Entrez votre adresse e-mail et votre nouveau mot de passe.</h2>

            <form @submit.prevent="handleResetPassword" class="space-y-4">
                <div>
                    <input v-model="form.email"
                            placeholder="E-mail"
                            required
                            class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber"
                    />
                </div>
                <div>
                    <input v-model="form.password"
                            type="password"
                            placeholder="Nouveau mot de passe"
                            required
                            class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber"
                    />
                </div>
                <div>
                    <input v-model="form.password2"
                            type="password"
                            placeholder="Confirmer le mot de passe"
                            required
                            class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber"
                    />
                </div>
                <p v-if="error" class="text-sm text-danger">{{ error }}</p>

                <BaseButton block type="submit">
                    Réinitialiser le mot de passe
                </BaseButton>
            </form>
        </div>
    </div>
</template>