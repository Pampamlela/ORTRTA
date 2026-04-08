<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useRollStore } from '@/stores/rolls';
import router from '@/router';
import api from '@/api/axios';

const route = useRoute()
const rollStore = useRollStore();
const qrCodeUrl = ref(null)

const revokeQrCodeUrl = () => {
    if (qrCodeUrl.value) {
        URL.revokeObjectURL(qrCodeUrl.value)
        qrCodeUrl.value = null
    }
}

const fetchQrCode = async (slug) => {
    revokeQrCodeUrl()
    const response = await api.get(`rolls/${slug}/qr/`, { responseType: 'blob' })
    qrCodeUrl.value = URL.createObjectURL(response.data)
}

onMounted(async() => {
    await rollStore.fetchRoll(route.params.slug);
    await fetchQrCode(route.params.slug)
})

onBeforeUnmount(() => {
    revokeQrCodeUrl()
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
    <div class="max-w-3xl mx-auto p-6">
        <div v-if="rollStore.currentRoll" class="space-y-6">

            <!-- HEADER -->
             <div class="bg-white shadow rounded-2xl p-6">
                <h1 class="text-2xl font-bold mb-2">
                    {{ rollStore.currentRoll.film_name }}
                </h1>
                <p class="text-gray-500">
                    {{ rollStore.currentRoll.format }} - ISO {{ rollStore.currentRoll.iso }}
                </p>
            </div>

            <!-- INFOS -->
             <div class="bg-white shadow rounded-2xl p-6 space-y-2">
                <p><span class="font-semibold">Appareil :</span> {{ rollStore.currentRoll.camera_name }}</p>
                <p><span class="font-semibold">Objectif :</span> {{ rollStore.currentRoll.lens_name || "objectif fixe" }}</p>
                <p><span class="font-semibold">Statut :</span> {{ rollStore.currentRoll.status }}</p>

                <div class="pt-2 border-t mt-2">
                    <p><span class="font-semibold">Date de début :</span> {{ rollStore.currentRoll.date_start }}</p>
                    <p v-if="rollStore.currentRoll.date_end">
                        <span class="font-semibold">Date de fin :</span> {{ rollStore.currentRoll.date_end }}
                    </p>
                    <p v-if="rollStore.currentRoll.date_development">
                        <span class="font-semibold">Date de développement :</span> {{ rollStore.currentRoll.date_development }}
                    </p>
                    <p v-if="rollStore.currentRoll.date_scan">
                        <span class="font-semibold">Date de scan :</span> {{ rollStore.currentRoll.date_scan }}
                    </p>
                </div>

                <p v-if="rollStore.currentRoll.description" class="pt-2 border-t mt-2">
                    <span class="font-semibold">Description :</span> {{ rollStore.currentRoll.description }}
                </p>
             </div>

            <!-- GALERIES -->
            <div class="bg-white shadow rounded-2xl p-6">
                <h2 class="text-lg font-semibold mb-3">Galeries</h2>

                <ul v-if="rollStore.currentRoll.photos.length" class="space-y-2">
                    <li v-for="photo in rollStore.currentRoll.photos" :key="photo.id">
                        <a
                            :href="photo.url"
                            target="_blank"
                            class="text-blue-600 hover:underline"
                        >
                            {{ providerLabels[photo.provider] }}
                        </a>
                    </li>
                </ul>
                <p v-else class="text-gray-500">Aucune galerie ajoutée.</p>
            </div>

            <!-- QR CODE -->
            <div class="bg-white shadow rounded-2xl p-6 text-center">
                <h2 class="text-lg font-semibold mb-4">QR Code</h2>

                <img 
                    class="mx-auto w-40"
                    :src="qrCodeUrl"
                    alt="QR Code"
                />

                <p class="text-sm text-gray-500 mt-3">
                    Scannez ce QR code pour accéder à la pellicule.
                </p>
            </div>

            <!-- ACTIONS -->
            <div class="flex gap-3">
                <router-link
                    :to="`/rolls/${rollStore.currentRoll.slug}/edit`"
                    class="px-4 py-2 bg-gray-200 rounded-xl hover:bg-gray-300"
                >
                    Modifier
                </router-link>
                <button
                    @click="deleteRoll"
                    class="px-4 py-2 bg-red-500 text-white rounded-xl hover:bg-red-600"
                >
                    Supprimer
                </button>
            </div> 
        </div>
        <p v-else class="text-center text-gray-500"> Chargement de la pellicule...</p>
        
    </div>
    <!-- <div class="roll-detail">
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
    <router-link to="/rolls">
        Mes pellicules
    </router-link>
    <router-link to="/cameras">
        Mes appareils photo
    </router-link>
    <router-link to="/lenses">
        Mes objectifs
    </router-link> -->
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