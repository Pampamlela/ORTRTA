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
    iso: 400,
    format: '35MM-12',
    camera: "",
    lens: "",
    date_start: "",
    description: "",
    type: "COLOR_NEGATIVE"
})

// const filteredLenses = computed(() => {
//     if (!form.value.camera) {
//         return []
//     }

//     return lensStore.lenses.filter(lens =>
//         lens.cameras.includes(form.value.camera)
//     )
// })

// const selectedCamera = computed(() => {
//     return cameraStore.cameras.find(cam => cam.id === form.value.camera);
// })

watch(() => form.value.camera, () => {
    form.value.lens = "";
})

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

            <RollForm
                :form="form"
                :submitLabel="'Créer'"
                :onSubmit="handleSubmit"
                :error="error"
            />
    </div>
</template>
       