<script setup>
import { onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import api from '@/api/axios';
import BaseButton from '@/components/BaseButton.vue';
// import PageContainer from '@/components/PageContainer.vue';

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
    
    <div class="px-4 py-6 max-w-5xl mx-auto flex flex-col md:grid md:grid-cols-2 md:gap-12 items-center"> 
        <!-- Colonne gauche : logo -->  
        <div class="hidden md:flex justify-center items-center">
            <img
            src="@/assets/logo/logo2.png" 
            alt="One Roll" 
            class="h-auto w-auto"
            />
        </div>

        <!-- Mobile : logo au dessus du titre -->
        <div class="flex justify-center md:hidden mb-4">
            <img
            src="@/assets/logo/logo2.png" 
            alt="One Roll" 
            class="h-48 w-auto mx-auto"
            />
        </div>

        <!-- Colonne droite : contenu -->
        <div>
            <h1 class="font-title text-2xl md:text-3xl mb-6 text-film">Profil</h1>

            <div v-if="loading">Chargement...</div>

            <div v-else class="space-y-4">
                <!-- Infos en lecture seule -->
                <div>
                    <!-- <label class="text-sm text-grain">Surnom</label> -->
                        <input :value="authStore.user?.username" type="text" disabled
                                class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber" />
                </div>
                <div>
                    <!-- <label class="text-sm text-grain">Email</label> -->
                        <input :value="authStore.user?.email" 
                                type="email" 
                                disabled 
                                class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber"
                        />
                </div>

                <!-- Formulaire mot de passe + actions -->
                <form @submit.prevent="handleChangePassword" class="space-y-4">
                    <div>
                        <!-- <label class="text-sm text-grain">Nouveau mot de passe</label> -->
                        <input 
                            v-model="password" 
                            type="password" 
                            placeholder="Nouveau mot de passe"
                            class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber" 
                        />
                    </div>
                    <div>
                        <!-- <label class="text-sm text-grain">Confirmer le mot de passe</label> -->
                        <input 
                            v-model="confirmPassword" 
                            type="password" 
                            placeholder="Confirmer le mot de passe" 
                            class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber"
                        />
                    </div>

                    <p v-if="error" class="error" style="color: red;">
                    {{ error }}
                    </p>
                    <p v-if="success" class="success" style="color: green;">
                        {{ success }}
                    </p>

                    <div class="flex gap-3">
                        <BaseButton block type="submit" :disabled="submitting">
                            {{ submitting ? "Modification..." : "Sauvegarder" }}
                        </BaseButton>
                        <BaseButton 
                            block
                            variant="danger"
                            type="button"
                            @click="handleDeleteAccount"
                            :disabled="deleting"
                        >
                            {{ deleting ? "Suppression..." : "Supprimer mon compte" }}
                        </BaseButton>
                    </div>
                </form>

                <p v-if="deleteError" class="error" style="color: red;">
                    {{ deleteError }}
                </p>

                <!-- actions secondaires -->
                <div class="flex gap-3 pt-2">
                    <BaseButton variant="outline" type="button" @click="exportData">
                        Exporter mes données
                    </BaseButton>
                    <!-- <BaseButton variant="outline" type="button" @click="logoutUser">
                        Se déconnecter
                    </BaseButton> -->
                </div>
          
            </div>
           
        </div> 
    </div>
</template>