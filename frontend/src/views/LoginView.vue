<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PageContainer from '@/components/PageContainer.vue';

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
    <PageContainer title="Connexion">
        
            <h1>Connexion</h1>

        <form @submit.prevent="handleLogin">
            <div>
                <label>Email</label>
                <input v-model="form.email" placeholder="Email" required />
            </div>

            <div>
                <label>Password</label>
                <input v-model="form.password" type="password" placeholder="Mot de passe" required />
            </div>

            <button type="submit">Se connecter</button>

            <p v-if="error" class="error">{{ error }}</p>
        </form>
    </PageContainer>
</template>

<style scoped>
.login-container {
    max-width: 400px;
    margin: 100px auto;
}

input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
}

button {
    width: 100%;
    padding: 10px;
    cursor: pointer;
}

.error {
    color: red;
    margin-top: 10px;
}
</style>