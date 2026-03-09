<script setup>
import { onMounted } from "vue";
import { useRollStore } from "@/stores/rolls";

const rollStore = useRollStore();
onMounted(() => {
  rollStore.fetchStats();
});
</script>

<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    
    <div v-if="rollStore.stats">
      <p>Total pellicules: {{ rollStore.stats.total_rolls }}</p>
      <p>En cours : {{ rollStore.stats.in_progress }}</p>
      <p>Terminées : {{ rollStore.stats.finished }}</p>
      <p>Développées : {{ rollStore.stats.developed }}</p>
      <p>Scannées : {{ rollStore.stats.scanned }}</p>
    </div>

    
    <p v-else>Chargement des statistiques...</p>

    <router-link to="/rolls">Voir mes pellicules</router-link>
    
  </div>
</template>
