<script setup>
import { onMounted } from 'vue';
import { useRollStore } from '@/stores/rolls';
import { useAuthStore } from '@/stores/auth';

import RollsTable from '@/components/RollsTable.vue';
import PageContainer from '@/components/PageContainer.vue';
import BaseButton from '@/components/BaseButton.vue';

const rollStore = useRollStore();
const authStore = useAuthStore();


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
        <RollsTable :rolls="rollStore.rolls" />

        <!-- Pagination -->
         <div class="flex justify-between items-center mt-6">
            <BaseButton
                :disabled="!rollStore.previous"
                @click="rollStore.fetchRolls(rollStore.previous)"
            >
                ← Page précédente
            </BaseButton>

            <span class="text-sm text-grain">
                {{ rollStore.rolls.length }} / {{ rollStore.count }} pellicules
            </span>

            <BaseButton
                :disabled="!rollStore.next"
                @click="rollStore.fetchRolls(rollStore.next)"
            >
                Page suivante →
            </BaseButton>
         </div>
    </PageContainer>
</template>
