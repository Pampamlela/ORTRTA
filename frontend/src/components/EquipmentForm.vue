<script setup>
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
            
            <!-- <div v-if="form.has_fixed_lens">
                <label>Objectif intégré</label>
                <input v-model="form.fixed_lens_model" placeholder="ex: 35mm f/2.8" />
            </div> -->
        </div>

        <label>Description</label>
        <textarea v-model="form.description"></textarea>

        <button 
            type="submit">{{ submitLabel }}
        </button>

        <p v-if="error" class="error">{{ error }}</p>
    </form>
</template>