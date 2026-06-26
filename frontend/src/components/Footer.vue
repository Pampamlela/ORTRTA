<script setup>
import router from '@/router';

</script>

<template>
    <footer class="bg-paper border-t border-gray-200 mt-10">
        <div class="maw-w-5xl mx-auto px-4 py-6 text-center text-sm text-grain">
            <p class="mb-2">
                One Roll To Rule Them All © 2026
            </p>

            <router-link
            to="/rgpd"
            class="text-amber underline"
            >
                Politique de confidentialité
            </router-link>
             - 
            <router-link
            to="/faq"
            class="text-amber underline"
            >
                FAQ
            </router-link>

        </div>
    </footer>
</template>