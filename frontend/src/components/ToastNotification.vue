<script setup>
import { useToastStore } from '@/stores/toast';
const toastStore = useToastStore();

const variantClasses = {
    success: 'bg-amber text-film',
    error: 'bg-danger text-white',
    warning: 'bg-yellow-500 text-black',
}
</script>

<template>
    <div class="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
        <div
            v-for="toast in toastStore.toasts"
            :key="toast.id"
            :class="['px-4 py-3 rouded-lg shadow-lg font-ui text-sm flex ites-center justify-between gap-4 min-w-64, variantClasses[toast.ttype]']"
        >
            <span>{{ toast.message }}</span>
            <button @click="toastStore.removeToast(toast.id)" class="opacity-70 hover:opacity-100">
                ✕
            </button>
        </div>
    </div>
</template>