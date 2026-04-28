<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useRollStore } from '@/stores/rolls';
import RollForm from '@/components/RollForm.vue';
import api from '@/api/axios';
import PageContainer from '@/components/PageContainer.vue';

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
    form.value.photos = roll.photos?.length
        ? roll.photos.map(photo => ({
            url: photo.url,
            provider: photo.provider || "OTHER",
        }))
        : [{ url: "", provider: "OTHER" }];
    await fetchQrCode(route.params.slug)

})

onUnmounted(() => {
    revokeQrCodeUrl()
})

const normalizeFormData = (data) => {
    const normalized = {
        ...data,
        date_end: data.date_end || null,
        date_development: data.date_development || null,
        date_scan: data.date_scan || null,
        photos: data.photos?.filter(p => p.url) || [] // remove empty photo URLs
    }
    console.log('Sending normalized data:', normalized);
    return normalized
}

const handleSubmit = async () => {
    try {
        const normalizedData = normalizeFormData(form.value);
        await rollStore.updateRoll(route.params.slug, normalizedData);

        router.push(`/rolls/${route.params.slug}`);
    } catch (err) {
        console.error('Update error:', err.response?.data || err);
        error.value = err.response?.data?.detail || "Erreur lors de la mise à jour de la pellicule."
    }
}
</script>

<template>
    <PageContainer title="Modifier la pellicule">
        <div class="max-w-lg mx-auto">
            <div class="flex items-center justify-end mb-6">
                <button
                    @click="showQR = !showQR"
                    class="bg-amber text-film px-4 py-2 rounded-xl text-sm font-ui shadow-sm"
                >
                    Voir QR Code
                </button>
            </div>

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
    </PageContainer>
</template>