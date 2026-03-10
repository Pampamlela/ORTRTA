<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useCameraStore } from '@/stores/cameras';
import router from '@/router';

const route = useRoute()
const cameraStore = useCameraStore();

onMounted(async() => {
    await cameraStore.fetchCamera(route.params.id);
})

const deleteCamera = async () => {
    if(!confirm("Êtes-vous sûr de vouloir supprimer cet appareil photo ? Cette action est irréversible.")) return

    try {
        await cameraStore.deleteCamera(route.params.id)
        router.push("/cameras")
    } catch (err) {
        alert("Erreur lors de la suppression de l'appareil photo.")
    }
}
</script>

<template>
    <div class="camera-detail">
        <div v-if="cameraStore.currentCamera">

            <h1>{{ cameraStore.currentCamera.model }}</h1>

            <p v-if="cameraStore.currentCamera.has_fixed_lens">
                <strong> Objectif fixe </strong> {{ cameraStore.currentCamera.fixed_lens_model }}
            </p>

            <p v-if="cameraStore.currentCamera.description">
                <strong> Description :</strong>{{ cameraStore.currentCamera.description }}
            </p>
            <p v-else>Aucune description disponible.</p>

            <router-link :to="`/cameras/${cameraStore.currentCamera.id}/edit`">
                Modifier
            </router-link>

            <button @click="deleteCamera">
                Supprimer
            </button>

        </div>

        <p v-else>Chargement de l'appareil photo...</p>
    </div>
    
    <router-link to="/cameras/new">
        Nouvel appareil photo
    </router-link>
    <router-link to="/rolls">
        Mes pellicules
    </router-link>
    <router-link to="/lenses">
        Mes objectifs
    </router-link> 
    <router-link to="/cameras">
        Mes appareils photo
    </router-link>

</template>

<style scoped>
.camera-detail {
    padding: 40px;
}
</style>