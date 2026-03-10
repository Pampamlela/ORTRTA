<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useRollStore } from '@/stores/rolls';
import RollForm from '@/components/RollForm.vue';

const router = useRouter();
const route = useRoute();
const rollStore = useRollStore();

const form = ref(null);
const error = ref(null);
onMounted(async () => {

    const roll = await rollStore.fetchRoll(route.params.slug);

    form.value = { ...roll };
})

const handleSubmit = async () => {
    try {
        await rollStore.updateRoll(route.params.slug, form.value);

        router.push(`/rolls/${route.params.slug}`);
    } catch (err) {
        error.value = "Erreur lors de la mise à jour de la pellicule."
    }
}
</script>

<template>
    <h1>Modifier la pellicule</h1>
    <RollForm 
        v-if="form"
        :form="form" 
        submitLabel="Modifier"
        :onSubmit="handleSubmit" 
        :error="error"      
    />
    <pre>{{ form }}</pre>
</template>