<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCameraStore } from '@/stores/cameras';
import PageContainer from '@/components/PageContainer.vue';
import BaseButton from '@/components/BaseButton.vue';

const router = useRouter();
const cameraStore = useCameraStore();

onMounted(() => {
    cameraStore.fetchCameras();
})
</script>

<template>
    <PageContainer title="Mes appareils photo">
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
        <BaseButton to="/lenses/new">
            + Objectif
        </BaseButton>
    
    </PageContainer>
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