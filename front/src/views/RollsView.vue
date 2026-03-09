<script setup>
import { onMounted } from 'vue';
import { useRollStore } from '@/stores/rolls';

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
            <!-- <strong>{{  roll.film_name }}</strong>
            <br>

            Appareil photo : {{  roll.camera_name }} <br>
            objectif : {{ roll.lens_name || "objectif fixe"}} <br>
            ISO : {{ roll.iso }} <br>
            statut : {{ roll.status }} <br>
            date de début : {{ roll.start_date }} <br>
            date de fin : {{ roll.end_date || "en cours" }} <br>
            date de développement : {{ roll.development_date || "non développée" }} <br>
            date de scan : {{ roll.scan_date || "non scannée" }} <br> -->
            <router-link :to="`/rolls/${roll.slug}`">
                <strong>{{ roll.film_name }}</strong><br>
                {{ roll.camera_name }} - ISO {{ roll.iso }} - {{ roll.status }}
            </router-link>
            <router-link to="/rolls/new">
                Nouvelle pellicule
            </router-link>
            </li>
        </ul>
        
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