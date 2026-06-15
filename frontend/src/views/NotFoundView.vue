<script setup>
import PageContainer from '@/components/PageContainer.vue';
import BaseButton from '@/components/BaseButton.vue';
</script>

<template>
    <PageContainer>
        <div class="flex flex-col items-center justify-center gap-6 py-20">
            <h1 class="font-title text-5xl text-film">404</h1>
            <p class="text-grain font-body">
                Oups!
                Cette page n'existe pas ou a été déplacée.
            </p>
            <BaseButton to="/rolls">
            Retour à l'accueil
            </BaseButton>
        </div>
    </PageContainer>
</template>