<script setup>
import { onMounted } from 'vue';
import { useMountStore } from '@/stores/mounts';
import { useCameraStore } from '@/stores/cameras';

const mountStore = useMountStore();
const cameraStore = useCameraStore();

onMounted(() => {
    mountStore.fetchMounts();
    cameraStore.fetchCameras();
})

const props = defineProps({
    form: Object,
    submitLabel: String,
    onSubmit: Function,
    error: String,
    type: String // "camera" ou "lens"
})
</script>

<template>
    <form @submit.prevent="onSubmit">

        <label>Modèle</label>
        <input v-model="form.model" type="text" required />

        <!-- spécifique aux caméras --->
        <div v-if="type === 'camera'">
            <input v-model="form.has_fixed_lens" type="checkbox" />
            <label>Objectif fixe</label>
            
            <div v-if="type === 'camera' && !form.has_fixed_lens">
                <label>Monture</label>
                <select v-model="form.mount">
                    <option disabled value="">Sélectionnez une monture</option>
                    <option 
                        v-for="mount in mountStore.mounts" 
                        :key="mount.id" 
                        :value="mount.id"
                    >
                        {{ mount.name }}
                    </option>
                </select>
            </div>
        </div>

        <!-- spécifique aux objectifs --->
        <div v-if="type === 'lens'">
            <label>Monture</label>
            <select v-model="form.mount">
                <option disabled value="">Sélectionnez une monture</option>
                <option 
                    v-for="mount in mountStore.mounts" 
                    :key="mount.id" 
                    :value="mount.id"
                >
                    {{ mount.name }}
                </option>
            </select>

            <label>Compatible avec</label>
            <select v-model="form.cameras_ids" multiple>
                <option 
                    v-for="camera in cameraStore.cameras" 
                    :key="camera.id" 
                    :value="camera.id"
                >
                    {{ camera.model }}
                </option>
            </select>
        </div>

        <label>Description</label>
        <textarea v-model="form.description"></textarea>

        <button 
            type="submit">{{ submitLabel }}
        </button>

        <p v-if="error" class="error">{{ error }}</p>
    </form>
    <pre>
        {{ form }}
    </pre>
</template>