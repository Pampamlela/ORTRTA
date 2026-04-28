<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useCameraStore } from '@/stores/cameras';
import router from '@/router';
import PageContainer from '@/components/PageContainer.vue';

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
    <PageContainer title="Détails de l'appareil photo">
        <div v-if="cameraStore.currentCamera">

            <h1>{{ cameraStore.currentCamera.model }}</h1>

            <p v-if="cameraStore.currentCamera.has_fixed_lens">
                <strong> Objectif fixe </strong> {{ cameraStore.currentCamera.fixed_lens_model }}
            </p>

            <p v-if="cameraStore.currentCamera.description">
                <strong> Description :</strong>{{ cameraStore.currentCamera.description }}
            </p>
            <p v-else>Aucune description disponible.</p>

            <h2>Objectifs compatibles</h2>
            <ul v-if="cameraStore.currentCamera.lenses?.length">
                <li v-for="lens in cameraStore.currentCamera.lenses" :key="lens">
                    <router-link :to="`/lenses/${lens.id}`">
                        {{ lens.model }}
                    </router-link>
                </li>
            </ul>
            <p v-else>Aucun objectif compatible pour le moment.</p>

            <router-link :to="`/cameras/${cameraStore.currentCamera.id}/edit`">
                Modifier
            </router-link>

            <button @click="deleteCamera">
                Supprimer
            </button>

        </div>

        <p v-else>Chargement de l'appareil photo...</p>
    
    
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

    </PageContainer>

</template>

<style scoped>
.camera-detail {
    padding: 40px;
}
</style>