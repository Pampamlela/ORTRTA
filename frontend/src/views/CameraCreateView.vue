<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useCameraStore } from '@/stores/cameras';
import EquipmentForm from '@/components/EquipmentForm.vue';

const router = useRouter();
const cameraStore = useCameraStore();

const form = ref({
    model: "",
    has_fixed_lens: false,
    fixed_lens_model:"",
    description: "",
    lenses_ids: [],
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

        <EquipmentForm 
            :form="form" 
            submitLabel="Créer"
            :onSubmit="handleSubmit" 
            :error="error"
            type="camera"
        />
    </div>
</template>