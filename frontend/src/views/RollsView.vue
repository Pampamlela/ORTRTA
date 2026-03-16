<script setup>
import { onMounted } from 'vue';
import { useRollStore } from '@/stores/rolls';
import router from '@/router';
import { useAuthStore } from '@/stores/auth';

const rollStore = useRollStore();

onMounted(() => {
  rollStore.fetchRolls();
});                 
</script>

<template>
    <div class="rolls">
        <h1>Mes pellicules</h1>

        <div v-if="rollStore.rolls.length === 0">
            Aucune pellicule pour le moment.
        </div>

        <ul v-else>
            <li v-for="roll in rollStore.rolls" :key="roll?.slug">

            <router-link :to="`/rolls/${roll.slug}`">
                <strong>{{ roll.film_name }}</strong><br>
                {{ roll.camera_name }} - ISO {{ roll.iso }} - {{ roll.status }}
            </router-link>
            <router-link to="/rolls/new">
                Nouvelle pellicule
            </router-link>
            </li>
        </ul>
        <router-link to="/cameras">
            Mes appareils photo
        </router-link>
        <router-link to="/lenses">
            Mes objectifs
        </router-link>
        <router-link to="/cameras/new">
            Nouvel appareil photo
        </router-link> 
        <router-link to="/lenses/new">
            Nouvel objectif
        </router-link>

        <button @click="authStore.logout()">Logout</button>
        
    </div>
</template>

<style scoped>
.rolls {
    padding: 40px;
}

li {
    margin-bottom: 20px;
    padding: 10px;
    border-bottom: 1px solid #ccc;
}
</style>