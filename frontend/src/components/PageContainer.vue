<script setup>
const props = defineProps({
    title: String,
    centered: {
        type: Boolean,
        default: false
    }
})
</script>

<template>
    <div class="px-4 py-6">
        <div
            :class="[
                'max-w-5xl mx-auto',
                centered ? 'text-center' : ''
            ]"
        >
        <!-- Titre -->
        <h1
        v-if="title"
        class="font-title text-2xl md:text-3xl mb-6 text-film"
        >
            {{ title }}
        </h1>
        <!-- Contenu -->
        <slot />
        </div>
    </div>
</template>