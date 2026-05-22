<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import BaseButton from '@/components/BaseButton.vue';

const router = useRouter();
const authStore = useAuthStore();

const form = ref({
    username: "",
    email: "",
    password: "",
    password2: "",
})

const error = ref(null)

const logoutUser = () => {
    authStore.logout();
    window.location.href = "/login";
}

const handleSubmit = async () => {
    try {
        await authStore.register(form.value)
        router.push("/rolls")
    } catch {
        error.value = "Erreur lors de l'inscription. Veuillez réessayer."
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
            <h1 class="font-title text-2xl md:text-3xl mb-6 text-film">Inscription</h1>

            <form @submit.prevent="handleSubmit" class="space-y-4">
                <div>
                    <!-- <label class="text-sm text-grain">Surnom</label> -->
                    <input v-model="form.username" 
                            placeholder="Surnom" 
                            required 
                            class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber" 
                    />
                </div>
                <div>
                    <!-- <label class="text-sm text-grain">Email</label> -->
                    <input v-model="form.email" 
                            type="email" 
                            placeholder="Email" 
                            required 
                            class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber" 
                    />
                </div>
                <div>
                    <!-- <label class="text-sm text-grain">Mot de passe</label> -->
                    <input v-model="form.password" 
                            type="password" 
                            placeholder="Mot de passe" 
                            required 
                            class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber" 
                    />
                </div>
                <div>
                    <!-- <label class="text-sm text-grain">Confirmer le mot de passe</label> -->
                    <input v-model="form.password2" 
                            type="password" 
                            placeholder="Confirmer le mot de passe" 
                            required 
                            class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber" 
                    />
                </div>
                <p v-if="error" class="text-sm text-danger">{{ error }}</p>

                <BaseButton block type="submit">
                    Valider
                </BaseButton>
            </form>

            <p class="text-xs text-grain mt-4">Vos données sont utilisées uniquement pour gérer votre compte, vos pellicules et votre matériel.</p>
            <p class="text-xs text-grain mt-4">En créant un compte, vous acceptez notre <router-link to="/rgpd">politique de confidentialité</router-link>.</p>

            <!-- <button @click="logoutUser" style="margin-top: 20px;">Se déconnecter</button> -->
        </div>
    </div>
</template>