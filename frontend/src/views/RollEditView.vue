<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useRollStore } from '@/stores/rolls';
import RollForm from '@/components/RollForm.vue';
import api from '@/api/axios';

const router = useRouter();
const route = useRoute();
const rollStore = useRollStore();
const qrCodeUrl = ref(null);
const showQR = ref(false);

const form = ref(null);
const error = ref(null);

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

onMounted(async () => {

    const roll = await rollStore.fetchRoll(route.params.slug);

    form.value = { ...roll };
    await fetchQrCode(route.params.slug)
})

const handleSubmit = async () => {
    try {
        await rollStore.updateRoll(route.params.slug, form.value);

        router.push(`/rolls/${route.params.slug}`);
    } catch (err) {
        error.value = "Erreur lors de la mise à jour de la pellicule."
    }
}
</script>

<template>
    <div class="min-h-screen bg-paper px-4 py-6">
        <div class="max-w-lg mx-auto "> <!--bg-white p-6 rounded-2xl shadow-sm pour faire ressortir le formulaire sur les grands écrans-->
            
            <div class="flex items-center justify-between mb-6">
                <h1 class="font-title text-2xl">Modifier la pellicule</h1>
                
                <button
                    @click="showQR = !showQR"
                    class="bg-amber text-film px-4 py-2 rounded-xl text-sm font-ui shadow-sm"
                    >
                    Voir QR Code
                </button>
            </div>

            <!-- QR Code -->
            <div v-if="showQR" class="mb-6 text-center bg-white p-4 rounded-xl shadow-sm">
                <img
                    v-if="qrCodeUrl"
                    class="mx-auto w-32"
                    :src="qrCodeUrl"
                    alt="QR Code de la pellicule"
                />
                <p v-else class="text-sm text-grain">Chargement du QR code...</p>
            </div>
            <RollForm 
                v-if="form"
                :form="form" 
                submitLabel="Modifier"
                :onSubmit="handleSubmit" 
                :error="error"      
            />
            
        </div>

    </div>
</template>