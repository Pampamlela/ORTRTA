<script setup>
// import { useRouter } from 'vue-router';
import { useRollStore } from '@/stores/rolls';

const rollStore = useRollStore();

const sortableFields = {
    film_name: "film_name",
    camera_name: "camera__model",
    status_label: "status_order",
    date_start: "date_start",
};

const sortIcon = (key) => {
    const field = sortableFields[key];
    if (!field) return ""; // pas d'icône pour les champs non triables

    const current = rollStore.ordering.startsWith("-")
        ? rollStore.ordering.slice(1)
        : rollStore.ordering;

    if (current !== field) return "↕";
    return rollStore.ordering.startsWith("-") ? "↓" : "↑";
}
const props = defineProps({
    rolls: Array,
    onRowClick: Function,
});

// const router = useRouter();

const rows = [
    { key : "film_name", label : "Film" },
    { key : "camera_name", label : "Appareil photo" },
    { key : "film_type_label", label : "Type"},
    { key : "iso", label : "ISO" },
    { key : "format", label : "Format" },
    { key : "photos", label : "Galeries" },
    { key : "description", label : "Description" },
    { key : "date_start" , label : "Début" },
    { key : "date_end", label : "Fin" },
    { key : "date_development", label : "Développement" },
    { key : "date_scan", label : "Scan" },
    { key : "status_label", label : "Statut" },
]

const formatValue = (roll, key) => {
    if (key === "photos") {
        return roll.photos?.length
        ? roll.photos[0].url
        : null;
    }

    if (key.includes("date") && roll[key]) {
        return new Date(roll[key]).toLocaleDateString();
    }

    return roll[key] || "-";
};

// const goToRoll = (slug) => {
//     router.push(`/rolls/${slug}/edit`); //on ne passe plus par la page détail
// };
</script>

<template>
    <div class="overflow-x-auto">
        <table class="border-collapse w-full text-sm">
            <tbody>
                <tr v-for="row in rows" :key="row.key">

                    <!--Colonne sticky à gauche-->
                    <td
                        class="sticky left-0 z-10 border border-black bg-amber text-film font-ui font-medium px-4 py-3 border-black min-w-[140px]"
                        >
                        <button
                            v-if="sortableFields[row.key]"
                            @click="rollStore.toggleOrdering(sortableFields[row.key])"
                            class="flex items-center gap-2 hover:underline"
                        >
                            {{ row.label }}
                            <span>{{ sortIcon(row.key) }}</span>
                        </button>
                        <span v-else>{{ row.label }}</span>       
                    </td>

                    <!--Colonnes rolls-->
                    <td
                        v-for="roll in rolls"
                        :key="roll.slug"
                        @click="props.onRowClick(roll.slug)"
                        class="border border-black px-4 py-3 min-w-[140px] cursor-pointer hover:bg-gray-50 transition font-body"
                    >
                    <!-- Cas galerie -->
                     <template v-if="row.key === 'photos'">
                        <a
                            v-if="formatValue(roll, row.key)"
                            :href="formatValue(roll, row.key)"
                            target="_blank"
                            class="text-blue-600 underline"
                            @click.stop
                        >
                            Voir
                        </a>
                        <span v-else>-</span>
                     </template>
                    
                    <!-- Cas normal -->
                     <template v-else>
                        <span
                            :class="{
                                'font-semibold': row.key === 'film_name'
                            }"
                        >
                            {{ formatValue(roll, row.key) }}
                        </span>
                     </template>

                    </td>

                </tr>
            </tbody>

        </table>

    </div>
</template>