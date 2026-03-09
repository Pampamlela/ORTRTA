<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useRollStore } from '@/stores/rolls';
import { onMounted } from 'vue';
import { useCameraStore } from '@/stores/cameras';

const router = useRouter();
const rollStore = useRollStore();
const cameraStore = useCameraStore();

onMounted(() => {
    cameraStore.fetchCameras();
})
const form = ref({
    film_name: "",
    iso: 400,
    format: '35MM-12',
    camera: "",
    date_start: "",
    description: "",
    type: "COLOR_NEGATIVE"
})
// const film_name = ref('');
// const iso = ref(400);
// const format = ref('35mm');
// const camera = ref(null);
// const date_start = ref('');
// const description = ref('');

const error = ref(null);

const handleSubmit = async () => {
    try {
        await rollStore.createRoll(form.value)

        router.push("/rolls");
    } catch (err) {
        console.log(err.response.data)
        error.value = "Erreur lors de la création de la pellicule";
    }
}
</script>

<template>
    <div class="roll-create">
        <h1>Nouvelle pellicule</h1>

        <form @submit.prevent="handleSubmit">

            <label>Nom de la pellicule</label>
            <input v-model="form.film_name" type="text" required />

            <label>ISO</label>
            <input v-model="form.iso" type="number" required />

            <label>Type</label>
            <select v-model="form.type" required>
                <option value="COLOR_NEGATIVE">Négatif couleur</option>
                <option value="BLACK_WHITE">Noir et blanc</option>
                <option value="SLIDE">Diapositive couleur</option>
            </select>

            <label>Format</label>
            <select v-model="form.format" required>
                <option value="35MM-12">35mm-12</option>
                <option value="35MM-24">35mm-24</option>
                <option value="35MM-36">35mm-36</option>

                <option value="120-04 (6x17)">120-04 (6x17)</option>
                <option value="120-06 (6x12)">120-06 (6x12)</option>
                <option value="120-08 (6x9)">120-08 (6x9)</option>
                <option value="120-09 (6x8)">120-09 (6x8)</option>
                <option value="120-10 (6x7)">120-10 (6x7)</option>
                <option value="120-12 (6x6)">120-12 (6x6)</option>
                <option value="120-26 (645)">120-26 (645)</option>
                
                <option value="220-08 (6x17)">220-08 (6x17)</option>
                <option value="220-12 (6x12)">220-12 (6x12)</option>
                <option value="220-16 (6x9)">220-16 (6x9)</option>
                <option value="220-18 (6x8)">220-18 (6x8)</option>
                <option value="220-20 (6x7)">220-20 (6x7)</option>
                <option value="220-24 (6x6)">220-24 (6x6)</option>
                <option value="220-32 (645)">220-32 (645)</option>

                <option value="LARGE-4x5">Grand format 4x5</option>
                <option value="LARGE-5x7">Grand format 5x7</option>
                <option value="LARGE-8x10">Grand format 8x10</option>

                <option value="110">110</option>
                <option value="126">126</option>
                <option value="127">127</option>
            </select>

            <label>ID appareil photo</label>
            <select v-model="form.camera" required>
                <option disabled value="">Sélectionnez un appareil photo</option>

                <option 
                    v-for="cam in cameraStore.cameras" 
                    :key="cam.id" 
                    :value="cam.id"
                >
                    {{ cam.model }}
                </option>
            </select>

            <label>Date de début</label>
            <input v-model="form.date_start" type="date" />

            <label>Description</label>
            <textarea v-model="form.description"></textarea>

            <button type="submit">Créer</button>

            <p v-if="error" class="error">{{ error }}</p>

        </form>

    </div>
</template>