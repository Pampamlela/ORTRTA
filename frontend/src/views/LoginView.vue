<template>
    <div class="login-container">
        <h1>Connexion</h1>

        <form @submit.prevent="handleLogin">
            <div>
                <label>Username</label>
                <input v-model="username" type="text" required />
            </div>

            <div>
                <label>Password</label>
                <input v-model="password" type="password" required />
            </div>

            <button type="submit">Se connecter</button>

            <p v-if="error" class="error">{{ error }}</p>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const password = ref('')
const error = ref('')

const auth = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
    error.value = null

    try {
        await auth.login(username.value, password.value)
        router.push('/')
    } catch (err) {
        error.value = 'Identifiants invalides'
    }
}
</script>

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