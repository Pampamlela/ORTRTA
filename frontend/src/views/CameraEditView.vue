<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useCameraStore } from '@/stores/cameras';
import EquipmentForm from '@/components/EquipmentForm.vue';

const router = useRouter();
const route = useRoute();
const cameraStore = useCameraStore();

const form = ref(null)
const error = ref(null);

onMounted(async () => {

    const camera = await cameraStore.fetchCamera(route.params.id);

    form.value = { ...camera };
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
    <div class="update-camera">
        <h1>Modifier l'appareil photo</h1>

        <EquipmentForm 
            v-if="form"
            :form="form" 
            submitLabel="Modifier"
            :onSubmit="handleSubmit" 
            :error="error"
            type="camera"
        />
    </div>
</template>