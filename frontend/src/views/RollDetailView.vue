<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useRollStore } from '@/stores/rolls';
import router from '@/router';

const route = useRoute()
const rollStore = useRollStore();

onMounted(async() => {
    await rollStore.fetchRoll(route.params.slug);
})

const deleteRoll = async () => {

    if(!confirm("Êtes-vous sûr de vouloir supprimer cette pellicule ? Cette action est irréversible.")) return 
    
    try {
        await rollStore.deleteRoll(route.params.slug)
        router.push("/rolls")
    } catch (err) {
        alert("Erreur lors de la suppression de la pellicule.")
    }
    

    
}
</script>

<template>
    <div class="roll-detail">
        <div v-if="rollStore.currentRoll">
            <h1> {{ rollStore.currentRoll.film_name }}</h1>

            <p><strong> Appareil Photo :</strong> {{ rollStore.currentRoll.camera_name }}</p>
            <p><strong> Objectif :</strong> {{ rollStore.currentRoll.lens_name || "objectif fixe" }}</p>
            
            <p><strong> ISO :</strong> {{ rollStore.currentRoll.iso }}</p>
            <p><strong> Format :</strong> {{ rollStore.currentRoll.format }}</p>

            <p><strong> Statut :</strong> {{ rollStore.currentRoll.status }}</p>

            <p><strong> Date de début :</strong> {{ rollStore.currentRoll.date_start }}</p>
            <p v-if="rollStore.currentRoll.date_end">
                <strong> Date de fin :</strong> {{ rollStore.currentRoll.date_end }}
            </p>

            <p v-if="rollStore.currentRoll.date_development">
                <strong> Date de développement :</strong> {{ rollStore.currentRoll.date_development }}
            </p>

            <p v-if="rollStore.currentRoll.date_scan">
                <strong> Date de scan :</strong> {{ rollStore.currentRoll.date_scan }}
            </p>

            <p v-if="rollStore.currentRoll.description">
                <strong> Description :</strong> {{ rollStore.currentRoll.description }}
            </p>

            <h2>Galeries</h2>

            <div v-if="rollStore.currentRoll.photos.length">

                <ul>
                    <li v-for="photo in rollStore.currentRoll.photos" :key="photo.id">
                        <a :href="photo.url" target="_blank">
                            {{ providerLabels[photo.provider] }}
                        </a>
                    </li>
                </ul>

            </div>

            <p v-else>Aucune galerie ajoutée.</p>

            <h2>QR Code</h2>

            <img 
                :src="`http://127.0.0.1:8000/api/rolls/${rollStore.currentRoll.slug}/qr/`"
                alt="QR Code pour partager la pellicule"
            />
            <p>
                Lien public :
                <a :href="`http://127.0.0.1:8000/r/${rollStore.currentRoll.slug}`">
                partager
                </a>
            </p>

            <router-link :to="`/rolls/${rollStore.currentRoll.slug}/edit`">
                Modifier
            </router-link>
            <button @click="deleteRoll">
                Supprimer
            </button>
        </div>

        <p v-else>Chargement...</p>
    </div>
</template>

<style scoped>
.roll-detail {
    padding: 40px;
}

img {
    margin-top: 20px;
    width: 200px;
}

</style>