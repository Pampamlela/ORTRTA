<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useLensStore } from '@/stores/lenses';
import router from '@/router';

const route = useRoute()
const lensStore = useLensStore();

onMounted(async() => {
    await lensStore.fetchLens(route.params.id);
})

const deleteLens = async () => {
    if(!confirm("Êtes-vous sûr de vouloir supprimer cet objectif ?")) return

    try {
        await lensStore.deleteLens(route.params.id)
        router.push("/lenses")
    } catch (err) {
        alert("Erreur lors de la suppression de l'objectif.")
    }
}
</script>

<template>
    <div class="lens-detail">
        <div v-if="lensStore.currentLens">
            <h1>{{ lensStore.currentLens.model }}</h1>
            <p v-if="lensStore.currentLens.description">
                <strong> Description :</strong>{{ lensStore.currentLens.description }}
            </p>
            <p v-else>Aucune description disponible.</p>

            <router-link :to="`/lenses/${lensStore.currentLens.id}/edit`">
                Modifier
            </router-link>
            <button @click="deleteLens">
                Supprimer
            </button>
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