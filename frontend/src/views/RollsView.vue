<script setup>
import { onMounted } from 'vue';
import { useRollStore } from '@/stores/rolls';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

import RollsTable from '@/components/RollsTable.vue';
import PageContainer from '@/components/PageContainer.vue';
import BaseButton from '@/components/BaseButton.vue';

const rollStore = useRollStore();
const authStore = useAuthStore();
const router = useRouter();
const goToRoll = (slug) => { router.push(`/rolls/${slug}/edit`); } //on ne passe plus par la page détail


onMounted(() => {
  rollStore.fetchRolls();
});    

const logoutUser = () => {
    authStore.logout();
    window.location.href = "/login";
}
</script>

<template>
    <PageContainer title="Pellicules">
        <!-- Cartes mobile -->
        <div class="md:hidden space-y-3">
            <div
                v-for="roll in rollStore.rolls"
                :key="roll.slug"
                class="bg-white rouded-lg p-4 shadow-sm cursor-pointer hover:shadow-md transition"
                @click="goToRoll(roll.slug)"
            >
                <div class="flex justify-between items-start mb-2">
                    <span class="font-semibold font-body text-film">{{ roll.film_name }}</span>
                    <span class="text-xs font-ui bg-amber text-film px-2 py-1 rouded-full">{{ roll.status_label }}</span>
                </div>
                <p class="text-sm text-grain font-body">{{  roll.camera_model }}</p>
                <p class="text-xs text-grain font-body mt-1">{{ new Date(roll.date_start). toLocaleDateString() }}</p>
            </div> 
        </div> 

        <!-- Tableau desktop -->
        <div class="hidden md:block">
            <RollsTable :rolls="rollStore.rolls" :onRowClick="goToRoll" />
        </div> 
        
        <!-- Pagination -->
         <div class="flex justify-between items-center mt-6">
            <BaseButton
                class="w-28"
                :disabled="!rollStore.previous"
                @click="rollStore.fetchRolls(rollStore.previous)"
            >
                <span class="flex flex-col items-center">
                   <span>←</span> 
                   <span>Page précédente</span>
                </span>
            </BaseButton>

            <span class="text-sm text-grain">
                {{ rollStore.rolls.length }} / {{ rollStore.count }} pellicules
            </span>

            <BaseButton
                class="w-28"
                :disabled="!rollStore.next"
                @click="rollStore.fetchRolls(rollStore.next)"
            >
                <span class="flex flex-col items-center">
                    <span>→</span>
                    <span>Page suivante</span>
                </span>
            </BaseButton>
         </div>
    </PageContainer>
</template>
