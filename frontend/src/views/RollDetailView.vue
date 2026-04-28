<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useRollStore } from '@/stores/rolls';
import router from '@/router';
import api from '@/api/axios';
import PageContainer from '@/components/PageContainer.vue';

const route = useRoute()
const rollStore = useRollStore();
const qrCodeUrl = ref(null)
const providerLabels = {
    FLICKR: "Flickr",
    GOOGLE_PHOTOS: "Google Photos",
    GOOGLE_DRIVE: "Google Drive",
    SITE: "Site personnel",
    OTHER: "Autre"
}

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
    <PageContainer title="Détails de la pellicule">

        <!-- HEADER -->
        <h1 class="font-title text-2xl mb-6">
            {{ rollStore.currentRoll?.film_name }}
        </h1>

        <div v-if="rollStore.currentRoll" class="space-y-4">

            <!-- INFOS -->
            <div class="bg-white p-4 rounded-xl shadow-sm space-y-3">
                <p><span class="font-ui">Appareil :</span> {{ rollStore.currentRoll.camera_name }}</p>
                <p><span class="font-ui">Objectif :</span> {{ rollStore.currentRoll.lens_name || "objectif fixe" }}</p>
                <p><span class="font-ui">ISO :</span> {{ rollStore.currentRoll.iso }}</p>
                <p><span class="font-ui">Format :</span> {{ rollStore.currentRoll.format }}</p>
                <p><span class="font-ui">Statut :</span> {{ rollStore.currentRoll.status }}</p>
            </div>

            <!-- DATES -->
            <div class="bg-white p-4 rounded-xl shadow-sm space-y-2 text-sm text-grain">
                <p>Début : {{ rollStore.currentRoll.date_start }}</p>
                <p v-if="rollStore.currentRoll.date_end">Fin : {{ rollStore.currentRoll.date_end }}</p>
                <p v-if="rollStore.currentRoll.date_development">Développement : {{ rollStore.currentRoll.date_development }}</p>
                <p v-if="rollStore.currentRoll.date_scan">Scan : {{ rollStore.currentRoll.date_scan }}</p>
            </div>

            <!-- DESCRIPTION -->
            <div v-if="rollStore.currentRoll.description"
                class="bg-white p-4 rounded-xl shadow-sm text-sm">
                {{ rollStore.currentRoll.description }}
            </div>

            <!-- GALERIES -->
            <div class="bg-white p-4 rounded-xl shadow-sm">
                <h2 class="font-ui mb-2">Galeries</h2>

                <ul v-if="rollStore.currentRoll.photos.length" class="space-y-1">
                <li v-for="photo in rollStore.currentRoll.photos" :key="photo.id">
                    <a :href="photo.url" target="_blank" class="text-amber underline">
                    {{ providerLabels[photo.provider] || photo.provider }}
                    </a>
                </li>
                </ul>

                <p v-else class="text-grain text-sm">Aucune galerie</p>
            </div>

                    <!-- QR CODE -->
            <div class="text-center">
                <h2 class="font-ui mb-2">
                    QR Code
                </h2>
                <img
                    class="mx-auto w-40"
                    :src="qrCodeUrl"
                    alt="QR Code pour partager la pellicule"
                />
            </div>

            <!-- ACTIONS -->
            <div class="flex gap-4 mt-6">

                <router-link
                :to="`/rolls/${rollStore.currentRoll.slug}/edit`"
                class="flex-1 text-center py-3 rounded-xl bg-amber text-film font-ui"
                >
                Modifier
                </router-link>

                <button
                @click="deleteRoll"
                class="flex-1 py-3 rounded-xl bg-danger text-white font-ui"
                >
                Supprimer
                </button>

            </div>

        </div>

        <p v-else>Chargement...</p>
    </PageContainer>
</template>
