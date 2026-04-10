<script setup>
import { ref, onMounted, computed, watch } from 'vue';
// import { useRouter } from 'vue-router';
// import { useRollStore } from '@/stores/rolls';
import { useCameraStore } from '@/stores/cameras';
import { useLensStore } from '@/stores/lenses';


// const router = useRouter();
// const rollStore = useRollStore();
const cameraStore = useCameraStore();
const lensStore = useLensStore();

const props = defineProps({
    form: Object,
    submitLabel: String,
    onSubmit: Function,
    error: String
})

const { form } = props;

onMounted(() => {
    cameraStore.fetchCameras();
    lensStore.fetchLenses();
})

const filteredLenses = computed(() => {
    if (!form.camera) return []

    const camera = cameraStore.cameras.find(
        cam => cam.id === form.camera
    );
    
    return lensStore.lenses.filter(lens => {
        // objectif spécifique à certains appareils
        if (lens.cameras?.length) {
            return lens.cameras.includes(camera.id);
        }

        // objectif à monture interchangeable
        return lens.mount === camera.mount;
    })
})

const selectedCamera = computed(() => {
    return cameraStore.cameras.find(cam => cam.id === form.camera);
})

watch(() => form.camera, () => {

    const camera = cameraStore.cameras.find(
        cam => cam.id === form.camera
    )
    if (camera?.has_fixed_lens) {
        form.lens = "";
    }   
})
    


</script>

<template>
    <form @submit.prevent="onSubmit" class="space-y-4 md:space-y-5">

        <!-- NOM -->
        <div>
        <label class="text-sm text-grain">Nom de la pellicule</label>
            <input v-model="form.film_name"
                    class="w-full p-3 rounded-lg bg-white border border-gray-200 focus:ring_amber" 
                    required/>
        </div>

        <!-- TYPE -->
        <div>
            <label class="text-sm text-grain">Type</label>
            <select v-model="form.film_type"
                    class="w-full p-3 rounded-lg bg-white border border-gray-200"
                    required>
                <option value="COLOR_NEGATIVE">Négatif couleur</option>
                <option value="BLACK_AND_WHITE">Noir et blanc</option>
                <option value="COLOR_SLIDE">Diapositive couleur</option>
            </select>
        </div>

        <!-- ISO -->
        <div>
            <label class="text-sm text-grain">ISO</label>
            <input v-model="form.iso" type="number" 
                    class="w-full p-3 rounded-lg bg-white border border-gray-200"
                    required />
        </div>

        <!-- FORMAT -->
        <div>
            <label class="text-sm text-grain">Format</label>
            <select v-model="form.format" 
                    class="w-full p-3 rounded-lg bg-white border border-gray-200"
                    required>
                <option value="35MM-12">35mm-12</option>
                <option value="35MM-24">35mm-24</option>
                <option value="35MM-36">35mm-36</option>

                <option value="120-04 (6x17)">120-04 (6x17)</option>
                <option value="120-06 (6x12)">120-06 (6x12)</option>
                <option value="120-08 (6x9)">120-08 (6x9)</option>
                <option value="120-09 (6x8)">120-09 (6x8)</option>
                <option value="120-10 (6x7)">120-10 (6x7)</option>
                <option value="120-12 (6x6)">120-12 (6x6)</option>
                <option value="120-26 (645)">120-26 (645)</option>
                
                <option value="220-08 (6x17)">220-08 (6x17)</option>
                <option value="220-12 (6x12)">220-12 (6x12)</option>
                <option value="220-16 (6x9)">220-16 (6x9)</option>
                <option value="220-18 (6x8)">220-18 (6x8)</option>
                <option value="220-20 (6x7)">220-20 (6x7)</option>
                <option value="220-24 (6x6)">220-24 (6x6)</option>
                <option value="220-32 (645)">220-32 (645)</option>

                <option value="LARGE-4x5">Grand format 4x5</option>
                <option value="LARGE-5x7">Grand format 5x7</option>
                <option value="LARGE-8x10">Grand format 8x10</option>

                <option value="110">110</option>
                <option value="126">126</option>
                <option value="127">127</option>
            </select>
        </div>

        <!-- CAMERA-->
        <div>
            <label class="text-sm text-grain">Appareil photo</label>
            <select v-model="form.camera" 
                    class="w-full p-3 rounded-lg bg-white border border-gray-200"
                    required>
                <option disabled value="">Sélectionnez un appareil photo</option>

                <option 
                    v-for="cam in cameraStore.cameras" 
                    :key="cam.id" 
                    :value="cam.id"
                >
                    {{ cam.model }}
                </option>
            </select>
        </div>

        <!-- LENS -->
        <div>
            <label class="text-sm text-grain">Objectif</label>
            <select v-model="form.lens"
                :disabled="selectedCamera?.has_fixed_lens"
                class="w-full p-3 rounded-lg bg-white border border-gray-200 disabled:bg-gray-100">
                <option disabled value="">
                    Sélectionnez un objectif
                </option>

                <option 
                    v-for="lens in filteredLenses" 
                    :key="lens.id" 
                    :value="lens.id"
                >
                    {{ lens.model }} {{ lens.mount_name }}
                </option>
            </select>

            <p v-if="selectedCamera?.has_fixed_lens"
                class="text-xs text-grain mt-1">
                Objectif fixe {{ selectedCamera.fixed_lens_model }}
            </p>
        </div>

        <!-- DATES -->
        <div class="grid grid-cols-1 gap-3">
            <label class="text-sm text-grain">Date de début</label>
            <input v-model="form.date_start" type="date" />

            <label class="text-sm text-grain">Date de fin</label>
            <input v-model="form.date_end" type="date" />

            <label class="text-sm text-grain">Date de développement</label>
            <input v-model="form.date_development" type="date" />

            <label class="text-sm text-grain">Date de scan</label>
            <input v-model="form.date_scan" type="date" />
        </div>

        <!-- DESCRIPTION -->
        <div>
            <label class="text-sm text-grain">Description</label>
            <textarea v-model="form.description"
                    class="w-full p-3 rounded-lg bg-white border border-gray-200 min-h-[100px]">
            </textarea>
        </div>

         <!-- GALERIES -->
        <div>
            <label class="text-sm text-grain">Galeries</label>
            <textarea v-model="form.photos"
                    class="w-full p-3 rounded-lg bg-white border border-gray-200 min-h-[100px]"
                    placeholder="Ajouter les URLs des galeries">
            </textarea>

        </div>


        <!-- ACTIONS -->
        <div class="flex gap-3 pt-4">

            <button type="submit"
                class="flex-1 py-3 rounded-xl bg-amber text-film font-ui">
                {{ props.submitLabel }}
            </button>

            <button type="button"
                class="flex-1 py-3 rounded-xl bg-danger text-white">
                Supprimer
            </button>
        </div>

        <p v-if="props.error" class="error">{{ props.error }}</p>

    </form>
</template>