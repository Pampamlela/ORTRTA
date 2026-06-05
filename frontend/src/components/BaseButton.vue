<script setup>
const props = defineProps({
    to: String,
    type: {
        type: String,
        default: "button",
    },
    variant: {
        type: String,
        default: "primary",
    },
    block: {
        type: Boolean,
        default: false,
    },
    disabled : {
        type: Boolean,
        default: false,
    }
})

const baseClasses = 
    "inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl font-ui text-sem transition"

const variants = {
    primary:
    "bg-amber text-film hover:opacity-90 shadow-sm",

    danger:
    "bg-danger text-white hover:opacity-90",

    outline:
    "border border-amber text-amber hover:bg-amber hover:text-film",

    ghost:
    "text-film hover:bg-gray-100",

}
</script>

<template>
    <!-- Router Link -->
    <router-link
        v-if="to && !disabled"
        :to="to"
        :class="[
            baseClasses,
            variants[variant],
            block ? 'w-full' : ''
        ]"
        >
        <slot />
    </router-link>

    <!-- Button -->
    <button
        v-else
        :type="type"
        :disabled="disabled"
        :class="[
            baseClasses,
            variants[variant],
            block ? 'w-full' : '',
            disabled ? 'opacity-50 cursor-not-allowed' : ''
        ]"
        >
        <slot />
     </button>
</template>