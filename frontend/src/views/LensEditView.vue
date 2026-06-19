<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router'; 
import { useLensStore } from '@/stores/lenses';
import EquipmentForm from '@/components/EquipmentForm.vue';
import PageContainer from '@/components/PageContainer.vue';
import { useToastStore } from '@/stores/toast';

const route = useRoute();
const router = useRouter();
const lensStore = useLensStore();
const toastStore = useToastStore();

const form = ref(null);
const error = ref(null);

onMounted(async () => {

    const lens = await lensStore.fetchLens(route.params.id);
    
    form.value = { ...lens };
})

const handleSubmit = async () => {
    try {
        await lensStore.updateLens(route.params.id, form.value);
        toastStore.addToast('Objectif mis à jour avec succès !');
        router.push('/cameras'); // avant `/lenses/${route.params.id}`
    } catch (err) {
        toastStore.addToast(
            err.response?.data?.detail || "Erreur lors de la mise à jour de l'objectif.",
            'error'
        );
    }
}

const handleDelete = async () => {
    if (!confirm("Êtes-vous sûr de vouloir supprimer cet objectif ? Cette action est irréversible.")) {
        return;
    }
    try {
        await lensStore.deleteLens(route.params.id);
        toastStore.addToast('Objectif supprimé avec succès !');
        router.push("/cameras");
    } catch (err) {
        toastStore.addToast(
            err.response?.data?.detail || "Erreur lors de la suppression de l'objectif.",
            'error'
        );
    }
}
</script>

<template>
    <PageContainer title="Modifier l'objectif">
        <div class="update-lens">
            <h1>Modifier l'objectif</h1>

            <EquipmentForm 
                v-if="form"
                :form="form" 
                submitLabel="Modifier"
                :onSubmit="handleSubmit" 
                :error="error"
                type="lens"
                :onDelete="handleDelete"
            />
        </div>
    </PageContainer>
</template>