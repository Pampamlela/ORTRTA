<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useCameraStore } from '@/stores/cameras';
import EquipmentForm from '@/components/EquipmentForm.vue';
import PageContainer from '@/components/PageContainer.vue';
import { useToastStore } from '@/stores/toast';

const router = useRouter();
const route = useRoute();
const cameraStore = useCameraStore();
const toastStore = useToastStore();

const form = ref(null)
const error = ref(null);

onMounted(async () => {

    const camera = await cameraStore.fetchCamera(route.params.id);

    form.value = { ...camera,
        lenses_ids: camera.lenses.map(lens => lens.id) || []
    };
})

const handleSubmit = async () => {
    try {
        await cameraStore.updateCamera(route.params.id, form.value);
        toastStore.addToast('Appareil photo mis à jour avec succès !');
        
        router.push("/cameras");
    } catch (err) {
        toastStore.addToast(
            err.response?.data?.detail || "Erreur lors de la mise à jour de l'appareil photo.",
            'error'
        );
        
    }
}

const handleDelete = async () => {
    if (!confirm("Êtes-vous sûr de vouloir supprimer cet appareil photo ? Cette action est irréversible.")) {
        return;
    }
    try {
        await cameraStore.deleteCamera(route.params.id);
        toastStore.addToast('Appareil photo supprimé avec succès !');
        router.push("/cameras");
    } catch (err) {
        toastStore.addToast(
            err.response?.data?.detail || "Erreur lors de la suppression de l'appareil photo.",
            'error'
        );
    }
}
</script>

<template>
    <PageContainer title="Modifier l'appareil photo">
        <EquipmentForm 
            v-if="form"
            :form="form" 
            submitLabel="Modifier"
            :onSubmit="handleSubmit" 
            :error="error"
            :onDelete="handleDelete"
            type="camera"
        />
    </PageContainer>
</template>