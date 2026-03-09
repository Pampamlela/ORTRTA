<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useCameraStore } from '@/stores/cameras';

const route = useRoute()
const cameraStore = useCameraStore();

onMounted(async() => {
    await cameraStore.fetchCamera(route.params.id);
})
</script>

<template>
    <div class="camera-detail">
        <div v-if="cameraStore.currentCamera">
            <h1>{{ cameraStore.currentCamera.model }}</h1>
            <p v-if="cameraStore.currentCamera.description">
                <strong> Description :</strong>{{ cameraStore.currentCamera.description }}
            </p>
            <p v-else>Aucune description disponible.</p>
        </div>

        <p v-else>Chargement de l'appareil photo...</p>
    </div>
    <router-link to="/cameras/new">
        Nouvel appareil photo
    </router-link>
</template>

<style scoped>
.camera-detail {
    padding: 40px;
}
</style>