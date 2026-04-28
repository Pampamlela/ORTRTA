<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useRollStore } from '@/stores/rolls';
import { useCameraStore } from '@/stores/cameras';
import { useLensStore } from '@/stores/lenses';
import RollForm from '@/components/RollForm.vue';

const router = useRouter();
const rollStore = useRollStore();
const cameraStore = useCameraStore();
const lensStore = useLensStore();

onMounted(() => {
    cameraStore.fetchCameras();
    lensStore.fetchLenses();
})
const form = ref({
    film_name: "",
    film_type: "COLOR_NEGATIVE",
    iso: 400,
    format: '35MM-12',
    camera: "",
    lens: "",
    date_start: "",
    date_end: "",
    date_development: "",
    date_scan: "",
    description: "",
    photos: [{ url: "", provider: "OTHER" }]
})



watch(() => form.value.camera, () => {
    form.value.lens = "";
})

const error = ref(null);

const normalizeFormData = (data) => {
    return {
        ...data,
        date_end: data.date_end || null,
        date_development: data.date_development || null,
        date_scan: data.date_scan || null,
        photos: data.photos?.filter(p => p.url) || [] // remove empty photo URLs
    }
}

const handleSubmit = async () => {
    try {
        const normalizedData = normalizeFormData(form.value);
        await rollStore.createRoll(normalizedData)

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

            <RollForm
                :form="form"
                :submitLabel="'Créer'"
                :onSubmit="handleSubmit"
                :error="error"
            />
    </div>
</template>
       