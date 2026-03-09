<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useCameraStore } from '@/stores/cameras';
import { onMounted } from 'vue';

const router = useRouter();
const cameraStore = useCameraStore();

// onMounted(() => {
//     cameraStore.fetchCameras();
// })
const form = ref({
    model: "",
    description: "",
})

const error = ref(null);

const handleSubmit = async () => {
    try {
        await cameraStore.createCamera(form.value)

        router.push("/cameras");
    } catch (err) {
        error.value = "Erreur lors de la création de l'appareil photo.";
    }
}
</script>

<template>
    <div class="camera-create">
        <h1>Nouvel appareil photo</h1>

        <form @submit.prevent="handleSubmit">

            <label>Modèle</label>
            <input v-model="form.model" type="text" required />

            <label>Description</label>
            <textarea v-model="form.description"></textarea>

            <button type="submit">Créer</button>

            <p v-if="error" class="error">{{ error }}</p>
            
        </form>

    </div>
</template>