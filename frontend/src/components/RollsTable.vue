<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
    rolls: Array
});

const router = useRouter();

const rows = [
    { key : "camera_name", label : "Appareil photo" },
    { key : "photos", label : "Galeries" },
    { key : "film_name", label : "Film" },
    { key : "film_type", label : "Type"},
    { key : "iso", label : "ISO" },
    { key : "format", label : "Format" },
    { key : "description", label : "Description" },
    { key : "date_start" , label : "Début" },
    { key : "date_end", label : "Fin" },
    { key : "date_development", label : "Développement" },
    { key : "date_scan", label : "Scan" },
    { key : "status", label : "Statut" },
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

const goToRoll = (slug) => {
    router.push(`/rolls/${slug}`);
};
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
                        {{ row.label }}
                    </td>

                    <!--Colonnes rolls-->
                    <td
                        v-for="roll in rolls"
                        :key="roll.slug"
                        @click="goToRoll(roll.slug)"
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