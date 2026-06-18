<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseButton from '@/components/BaseButton.vue';

const authStore = useAuthStore()
const router = useRouter()

const form = ref({
    email: '',
    password: '',
})
const error = ref(null)

const handleLogin = async () => {

    try {
        await authStore.login(form.value)
        router.push('/rolls')
    } catch {
        error.value = 'Identifiants invalides'
    }
}

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
            <h1 class="font-title text-2xl md:text-3xl mb-6 text-film">Connexion</h1>

            <form @submit.prevent="handleLogin" class="space-y-4">
                <div>
                    <!-- <label>E-mail</label> -->
                    <input v-model="form.email" 
                            placeholder="E-mail" 
                            required 
                            class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber" 
                    />
                </div>

                <div>
                    <!-- <label>Password</label> -->
                    <input v-model="form.password" 
                            type="password" 
                            placeholder="Mot de passe" 
                            required 
                            class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber" 
                    />
                </div>

                <div>
                    <router-link to="/forgot-password" class="text-sm text-grain hover:text-amber">
                        Mot de passe oublié ?
                    </router-link>
                </div>
                <p v-if="error" class="text-sm text-danger">{{ error }}</p>

                <BaseButton block type="submit">
                    Se connecter
                </BaseButton>

                
            </form>
        </div>
    </div>
</template>
