<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useCameraStore } from '@/stores/cameras';
import EquipmentForm from '@/components/EquipmentForm.vue';
import PageContainer from '@/components/PageContainer.vue';

const router = useRouter();
const route = useRoute();
const cameraStore = useCameraStore();

const form = ref(null)
const error = ref(null);

onMounted(async () => {

    const camera = await cameraStore.fetchCamera(route.params.id);

    form.value = { ...camera,
        lenses_ids: camera.lenses.map(lens => lens.id) || []
    };
})

const handleSubmit = async () => {
    try {
        await cameraStore.updateCamera(route.params.id, form.value);

        router.push("/cameras");
    } catch (err) {
        error.value = "Erreur lors de la mise à jour de l'appareil photo.";
    }
}
</script>

<template>
    <PageContainer title="Modifier l'appareil photo">
        <EquipmentForm 
            v-if="form"
            :form="form" 
            submitLabel="Modifier"
            :onSubmit="handleSubmit" 
            :error="error"
            type="camera"
        />
    </PageContainer>
</template>