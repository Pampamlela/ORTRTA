<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import PageContainer from '@/components/PageContainer.vue';

const router = useRouter();
const authStore = useAuthStore();

const form = ref({
    username: "",
    email: "",
    password: "",
    password2: "",
})

const error = ref(null)

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
    <PageContainer title="Inscription">
        
            <h1>Créer un compte</h1>

        <form @submit.prevent="handleSubmit">
            <input v-model="form.username" placeholder="Surnom" required />
            <input v-model="form.email" type="email" placeholder="Email" required />
            <input v-model="form.password" type="password" placeholder="Mot de passe" required />
            <input v-model="form.password2" type="password" placeholder="Confirmer le mot de passe" required />
            <button type="submit">S'inscrire</button>
        </form>
        <p>Vos données sont utilisées uniquement pour gérer votre compte, vos pellicules et votre matériel.</p>
        <p>En créant un compte, vous acceptez notre <router-link to="/rgpd">politique de confidentialité</router-link>.</p>
        <p v-if="error" class="error">{{ error }}</p>
    </PageContainer>
</template>