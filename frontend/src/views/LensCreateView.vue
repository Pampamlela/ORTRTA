<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useLensStore } from '@/stores/lenses';
import { useCameraStore } from '@/stores/cameras';
import { onMounted } from 'vue';

const router = useRouter();
const lensStore = useLensStore();
const cameraStore = useCameraStore();

onMounted(() => {
    lensStore.fetchLenses();
    cameraStore.fetchCameras();
})
const form = ref({
    model: '',
    camera:[],
    description: '',
});

const error = ref(null);

const handleSubmit = async () => {
    try {
        await lensStore.createLens(form.value)

        router.push("/lenses");
    } catch (err) {
        error.value = "Erreur lors de la création de l'objectif";
    }
}
</script>

<template>
    <div class="lens-create">
        <h1>Nouvel objectif</h1>

        <form @submit.prevent="handleSubmit">

            <label>Modèle</label>
            <input v-model="form.model" type="text" required />

            <select v-model="form.cameras" multiple>
                <option
                v-for="camera in cameraStore.cameras"
                :key="camera.id"
                :value="camera.id"
                >
                {{ camera.model }}
                </option>
            </select>
            <label>Description</label>
            <textarea v-model="form.description"></textarea>

            <button type="submit">Créer l'objectif</button>

            <p v-if="error" class="error">{{ error }}</p>
        </form>
    </div>
</template>