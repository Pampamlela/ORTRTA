<script setup>
import { onMounted } from "vue";
import { useRollStore } from "@/stores/rolls";
import { useAuthStore } from "@/stores/auth";
import PageContainer from '@/components/PageContainer.vue';
import BaseButton from "@/components/BaseButton.vue";

const rollStore = useRollStore();
const authStore = useAuthStore();

onMounted(() => {
  rollStore.fetchStats();
});

// labels lisibles pour les types de film
const filmTypeLabels = {
  COLOR_NEGATIVE: "Négatif couleur",
  BLACK_AND_WHITE: "Noir et blanc",
  COLOR_SLIDE: "Diapositive couleur",
}
</script>

<template>
  <PageContainer>
    <!-- Message de bienvenue -->
    <p v-if="authStore.user" class="font-title text-2xl text-film mb-8">
      Bienvenue sur votre tableau de bord, {{ authStore.user.username }}!
    </p> 
    
    <div v-if="rollStore.stats">

      <!-- Lige 1 : compteurs par statut-->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white rounded-lg p-4 text-center shadow-sm">
          <p class="font-title text-3xl text-film">{{ rollStore.stats.total_rolls }}</p>
          <p class="text-sm text-grain font-ui mt-1">Total</p>
        </div>
        <div class="bg-white rounded-lg p-4 text-center shadow-sm">
          <p class="font-title text-3xl text-amber">{{ rollStore.stats.in_progress }}</p>
          <p class="text-sm text-grain font-ui mt-1">En cours</p>
        </div>
        <div class="bg-white rounded-lg p-4 text-center shadow-sm">
          <p class="font-title text-3xl text-film">{{ rollStore.stats.finished }}</p>
          <p class="text-sm text-grain font-ui mt-1">Terminées</p>
        </div>
        <div class="bg-white rounded-lg p-4 text-center shadow-sm">
          <p class="font-title text-3xl text-film">{{ rollStore.stats.developed }}</p>
          <p class="text-sm text-grain font-ui mt-1">Développées</p>
        </div>
      </div>

      <!-- Ligne 2 : ISO moyen + répartition par type-->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <div class="bg-white rounded_lg p-4 shadow-sm">
          <p class="text-sm text-grain font-ui mb-2">ISO moyen</p>
          <p class="font-title text-3xl text-film">
            {{ Math.round(rollStore.stats.average_iso) }}
          </p>
        </div>
        <div class="bg-white rounded-lg p-4 shadow-sm">
          <p class="text-sm text-grain font-ui mb-3">Répartition par type de film</p>
          <ul class="space-y-2">
            <li
              v-for="item in rollStore.stats.by_film_type"
              :key="item.film_type"
              class="flex justify-between text-sm font-body text-film"
            >
              <span>{{ filmTypeLabels[item.film_type] || item.film_type }}</span>
              <span class="font-semibold">{{ item.count }}</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- lien vers les pellicules -->
      <BaseButton to="/rolls">
        Voir mes pellicules
      </BaseButton>
    </div>
    <!-- </div> 
      <p>Total pellicules: {{ rollStore.stats.total_rolls }}</p>
      <p>En cours : {{ rollStore.stats.in_progress }}</p>
      <p>Terminées : {{ rollStore.stats.finished }}</p>
      <p>Développées : {{ rollStore.stats.developed }}</p>
      <p>Scannées : {{ rollStore.stats.scanned }}</p>
    </div> -->

    
    <p v-else class="text-grain font-body">Chargement des statistiques...</p>

    <!-- <router-link to="/rolls">Voir mes pellicules</router-link> -->
    
  </PageContainer>
</template>
