<script setup>
import { onMounted } from 'vue';
import { useRollStore } from '@/stores/rolls';
import router from '@/router';
import { useAuthStore } from '@/stores/auth';
import api from '@/api/axios';
import RollsTable from '@/components/RollsTable.vue';
const rollStore = useRollStore();
const authStore = useAuthStore();

// const rows = [
//     { key : "camera_name", label : "Appareil photo" },
//     { key : "photos", label : "Galeries" },
//     { key : "film_name", label : "Film" },
//     { key : "film_type", label : "Type"},
//     { key : "iso", label : "ISO" },
//     { key : "format", label : "Format" },
//     { key : "description", label : "Description" },
//     { key : "date_start" , label : "Début" },
//     { key : "date_end", label : "Fin" },
//     { key : "date_development", label : "Développement" },
//     { key : "date_scan", label : "Scan" },
//     { key : "status", label : "Statut" },
// ]

// const formatValue = (roll, key) => {
//     if (key === "photos") {
//         return roll.photos?.length
//         ? "Voir"
//         : "-";
//     }

//     if (key.includes("date") && roll[key]) {
//         return new Date(roll[key]).toLocaleDateString();
//     }

//     return roll[key] || "-";
// }

onMounted(() => {
  rollStore.fetchRolls();
});    

const logoutUser = () => {
    authStore.logout();
    window.location.href = "/login";
}
</script>

<template>
    <div class="p-4">
        <h1 class="text-xl font-title mb-6">Pellicules</h1>

        <RollsTable :rolls="rollStore.rolls" />
    </div>
    <!-- <div class="overflow-x-auto">
        <table class="min-w-full border-collapse">

            <tbody>
                <tr v-for="row in rows" :key="row.key">

                     Colonne labels
                    <td class="bg-amber border px-3 py-2 font-medium">
                        {{ row.label }}
                    </td>

                     Colonnes rolls
                    <td
                    v-for="roll in rollStore.rolls"
                    :key="roll.slug"
                    class="bg-white border px-3 py-2"
                    >
                    {{ formatValue(roll, row.key) }}
                    </td>

                </tr>
            </tbody>

        </table>

    </div> -->
</template>
