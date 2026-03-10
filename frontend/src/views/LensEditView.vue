<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router'; 
import { useLensStore } from '@/stores/lenses';
import EquipmentForm from '@/components/EquipmentForm.vue';

const route = useRoute();
const router = useRouter();
const lensStore = useLensStore();

const form = ref(null);
const error = ref(null);

onMounted(async () => {

    const lens = await lensStore.fetchLens(route.params.id);
    
    form.value = { ...lens };
})

const handleSubmit = async () => {
    try {
        await lensStore.updateLens(route.params.id, form.value);
        router.push(`/lenses/${route.params.id}`);
    } catch (err) {
        error.value = "Erreur lors de la mise à jour de l'objectif.";
    }
}
</script>

<template>
    <div class="update-lens">
        <h1>Modifier l'objectif</h1>

        <EquipmentForm 
            v-if="form"
            :form="form" 
            submitLabel="Modifier"
            :onSubmit="handleSubmit" 
            :error="error"
            type="lens"
        />
    </div>
</template>