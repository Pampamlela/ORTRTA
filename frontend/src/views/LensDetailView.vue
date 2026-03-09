<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useLensStore } from '@/stores/lenses';

const route = useRoute()
const lensStore = useLensStore();

onMounted(async() => {
    await lensStore.fetchLens(route.params.id);
})
</script>

<template>
    <div class="lens-detail">
        <div v-if="lensStore.currentLens">
            <h1>{{ lensStore.currentLens.model }}</h1>
            <p v-if="lensStore.currentLens.description">
                <strong> Description :</strong>{{ lensStore.currentLens.description }}
            </p>
            <p v-else>Aucune description disponible.</p>
        </div>

        <p v-else>Chargement de l'objectif...</p>
    </div>
    <router-link to="/lenses/new">
        Nouvel objectif
    </router-link>
    <router-link to="/cameras/new">
        Nouvel appareil photo
    </router-link>
</template>

<style scoped>
.lens-detail {
    padding: 40px;
}   
</style>