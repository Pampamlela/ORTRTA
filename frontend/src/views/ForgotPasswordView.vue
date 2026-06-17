<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseButton from '@/components/BaseButton.vue';

const authStore = useAuthStore()
const router = useRouter()

const form = ref({
    email: '',
})

const error = ref(null)

const handleForgotPassword = async () => {
    try {
        await authStore.forgotPassword(form.value)
        router.push('/reset-password')
    } catch {
        error.value = 'Erreur lors de la demande de réinitialisation du mot de passe'
    }
}   

</script>

<template>
    <div class="px-4 py-6 max-w-5xl mx-auto flex flex-col md:grid md:grid-cols-2 md:gap-12 items-center">
        <!-- Colonne gauche : logo-->
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
            <h1 class="font-title text-2xl md:text-3xl mb-6 text-film">Réinitialiser le mot de passe.</h1>
            <h2 class="font-title text-sm md:text-xl mb-6 text-grain">Entrez votre adresse e-mail pour recevoir un lien de réinitialisation.</h2>

            <form @submit.prevent="handleForgotPassword" class="space-y-4">
                <div>
                    <input v-model="form.email"
                            placeholder="E-mail"
                            required
                            class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber"
                    />
                </div>
                <p v-if="error" class="text-sm text-danger">{{ error }}</p>

                <BaseButton block type="submit">
                    Demander la réinitialisation
                </BaseButton>

            </form>
        </div>

    </div>
</template>