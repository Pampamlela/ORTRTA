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
        <!-- <div class="flex gap-3">
            <BaseButton to="/rolls/new">
                + Pellicule
            </BaseButton>

            <BaseButton to="/cameras/new">
                + Appareil
            </BaseButton>
        </div> -->
        <RollsTable :rolls="rollStore.rolls" />
    </PageContainer>
</template>
