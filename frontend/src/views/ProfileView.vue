<script setup>
import { onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import api from '@/api/axios';

const authStore = useAuthStore();

const loading = ref(true);
const password = ref('');
const confirmPassword = ref('');

const error = ref(null);
const success = ref(null);
const submitting = ref(false);

onMounted(async() => {
    try {
        await authStore.fetchUser();
    } catch (e) {
        console.error("Erreur lors de la récupération du profil :", e);
    } finally {
        loading.value = false;
    }
});


const handleChangePassword = async () => {
    error.value = null;
    success.value = null;

    // validation frontend
    if (password.value !== confirmPassword.value) {
        error.value = "Les mots de passe ne correspondent pas.";
        return;
    }

    if (password.value.length < 8) {
        error.value = "Le mot de passe doit contenir au moins 8 caractères.";
        return;
    }

    submitting.value = true;

    try {
        await api.put('change-password/', {
            password: password.value,
        });

        success.value = "Mot de passe changé avec succès.";
        password.value = '';
        confirmPassword.value = '';
        // après changement
        authStore.logout();
        window.location.href = "/login";
    } catch (err) {
        // gestion DRF errors
        if (err.response?.data?.password) {
            error.value = err.response.data.password.join(' ');
        } else {
            error.value = "Une erreur est survenue. Veuillez réessayer.";
        }
    } finally {
        submitting.value = false;
    }
};

const deleting = ref(false);
const deleteError = ref(null);

const handleDeleteAccount = async () => {
    deleteError.value = null;

    const confirmed = confirm("Êtes-vous sûr de vouloir supprimer votre compte ? Cette action est irréversible.");

    if (!confirmed) return;

    deleting.value = true;

    try {
        await api.delete('me/');

        authStore.logout(); //netoyage de la session

        //redirection
        window.location.href = '/login';

    } catch (err) {
        deleteError.value = "Une erreur est survenue lors de la suppression du compte. Veuillez réessayer.";
    } finally {
        deleting.value = false;
    }
}

const logoutUser = () => {
    authStore.logout();
    window.location.href = "/login";
}

const exportData = async () => {
    try {
        const response = await api.get('me/export/',
            { headers : {
                Authorization: `Bearer ${authStore.accessToken}`,
            },
            }
        );

        const dataStr = JSON.stringify(response.data, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'my_data.json';
        link.click();
        window.URL.revokeObjectURL(url);

        // Gérer la réponse, par exemple en sauvegardant les données dans un fichier
        console.log("Données exportées :", response.data);
    } catch (err) {
        console.error("Erreur lors de l'export des données :", err);
    }
    return {exportData};
}
</script>

<template>
    <div class="profile">
        <h1>Profil</h1>

        <div v-if="loading">Chargement...</div>

        <div v-else>
            <p>Surnom: {{ authStore.user?.username }}</p>
            <p>Email: {{ authStore.user?.email }}</p>
        </div>
        
        <h2>Modifier le mot de passe</h2>

        <form @submit.prevent="handleChangePassword">
            <input 
                v-model="password" 
                type="password" 
                placeholder="Nouveau mot de passe" 
            />
            <input 
                v-model="confirmPassword" 
                type="password" 
                placeholder="Confirmer le mot de passe" 
            />

            <button :disabled="submitting">
                {{ submitting ? "Modifiction..." : "Changer le mot de passe" }} 
            </button>
        </form>

        <p v-if="error" class="error" style="color: red;">
            {{ error }}
        </p>
        <p v-if="success" class="success" style="color: green;">
            {{ success }}
        </p>

        <h2>Supprimer le compte</h2>
        <button 
            @click="handleDeleteAccount"
            :disabled="deleting"
        >
            {{ deleting ? "Suppression..." : "Supprimer mon compte" }}
        </button>

        <p v-if="deleteError" class="error" style="color: red;">
            {{ deleteError }}
        </p>

        <button @click="exportData">Exporter mes données</button>

        <button @click="logoutUser" style="margin-top: 20px;">Se déconnecter</button>
    </div>
</template>