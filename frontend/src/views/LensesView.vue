<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useLensStore } from '@/stores/lenses';

const router = useRouter();
const lensStore = useLensStore();

onMounted(() => {
    lensStore.fetchLenses();
})
</script>

<template>
    <div class="lenses">
        <h1>Mes objectifs</h1>

        <div v-if="lensStore.lenses.length === 0">
            Aucun objectif pour le moment.  
        </div>

        <ul v-else>
            <li v-for="lens in lensStore.lenses" :key="lens?.id">
                <router-link :to="`/lenses/${lens.id}`">
                    <strong>{{ lens.model }}</strong>
                </router-link>
            </li>
        </ul>
        <router-link to="/lenses/new">
            Nouvel objectif
        </router-link>
    </div>
</template>

<style scoped>
.lenses {
    padding: 40px;
}
li {
    margin-bottom: 20px;
    padding: 10px;
    border-bottom: 1px solid #ccc;
}
</style>