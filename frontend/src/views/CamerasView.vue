<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCameraStore } from '@/stores/cameras';

const router = useRouter();
const cameraStore = useCameraStore();

onMounted(() => {
    cameraStore.fetchCameras();
})
</script>

<template>
    <div class="cameras">
        <h1>Mes appareils photo</h1>

        <div v-if="cameraStore.cameras.length === 0">
            Aucun appareil photo pour le moment.
        </div>

        <ul v-else>
            <li v-for="camera in cameraStore.cameras" :key="camera.id">
                <router-link :to="`/cameras/${camera.id}`">
                    <strong>{{ camera.model }}</strong>
                </router-link>
                
            </li>
        </ul>
        <router-link to="/cameras/new">
            Nouvel appareil photo
        </router-link>
        <router-link to="/lenses/new">
            Nouvel objectif
        </router-link>
        <router-link to="/rolls/new">
            Nouvelle pellicule
        </router-link>
    </div>
</template>

<style scoped>
.cameras {
    padding: 40px;
}
li {
    margin-bottom: 20px;
    padding: 10px;
    border-bottom: 1px solid #ccc;
}
</style>