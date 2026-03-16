<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useLensStore } from '@/stores/lenses';
import EquipmentForm from '@/components/EquipmentForm.vue';

const router = useRouter();
const lensStore = useLensStore();

const form = ref({
    model: '',
    description: '',
    mount:'',
    cameras_ids: []
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

        <EquipmentForm 
            :form="form" 
            submitLabel="Créer"
            :onSubmit="handleSubmit" 
            :error="error"
            type="lens"
        />
    </div>
</template>