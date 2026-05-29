<script setup>
import { onMounted } from 'vue';
import { useMountStore } from '@/stores/mounts';
import { useCameraStore } from '@/stores/cameras';
import { useLensStore } from '@/stores/lenses';
import BaseButton from '@/components/BaseButton.vue';

const mountStore = useMountStore();
const cameraStore = useCameraStore();
const lensStore = useLensStore();

onMounted(() => {
    mountStore.fetchMounts();
    cameraStore.fetchCameras();
    lensStore.fetchLenses();
})

const props = defineProps({
    form: Object,
    submitLabel: String,
    onSubmit: Function,
    error: String,
    type: String // "camera" ou "lens"
})
</script>

<template>
    <form @submit.prevent="onSubmit" class="space-y-4">
        <!-- Champ commun : Modèle -->
        <div>
            <label class="text-sm text-grain">Modèle</label>
            <input 
                v-model="form.model" 
                type="text" 
                required 
                class="w-full p-3 rounded-lg bg-white border border-gray-200"
                />
        </div>

        <!-- spécifique aux caméras --->
        <div v-if="type === 'camera'">

            <div class="flex items-center gap-2 mb-4">
                <input 
                    v-model="form.has_fixed_lens" 
                    type="checkbox" 
                    id="has_fixed_lens"
                />
                <label for="has_fixed_lens" class="text-sm text-grain">
                    Objectif fixe
                </label>
            </div>

            <div v-if="!form.has_fixed_lens" class="space-y-4">
                <div>
                    <label class="text-sm text-grain">
                        Monture
                    </label>
                    <select
                        v-model="form.mount"
                        class="w-full p-3 rounded-lg bg-white border border-gray-200"
                    >
                        <option disabled value="">Sélectionnez une monture</option>
                        <option
                            v-for="mount in mountStore.mounts"
                            :key="mount.id"
                            :value="mount.id"
                        >
                            {{ mount.name }}
                        </option>
                    </select>
                </div>

                <div>
                    <label class="text-sm text-grain">Objectifs compatibles</label>
                    <select
                        v-model="form.lenses_ids"
                        multiple
                        class="w-full p-3 rounded-lg bg-white border border-gray-200"
                    >
                        <option
                            v-for="lens in lensStore.lenses"
                            :key="lens.id"
                            :value="lens.id"
                        >
                            {{ lens.model }}
                        </option>
                    </select>
                    <p class="text-xs text-grain mt-1">
                        Maintenez la touche Ctrl (ou Cmd sur Mac) pour sélectionner plusieurs objectifs.
                    </p>
                </div>
            </div>
        </div>
                
                <!-- <div v-if="type === 'camera' && !form.has_fixed_lens">
                    <label>Objectifs compatibles</label>
                    <select v-model="form.lenses_ids" multiple>
                        <option 
                            v-for="lens in lensStore.lenses" 
                            :key="lens.id" 
                            :value="lens.id"
                        >
                            {{ lens.model }}
                        </option>
                    </select>

                    <label>Monture</label>
                    <select v-model="form.mount">
                        <option disabled value="">Sélectionnez une monture</option>
                        <option 
                            v-for="mount in mountStore.mounts" 
                            :key="mount.id" 
                            :value="mount.id"
                        >
                            {{ mount.name }}
                        </option>
                    </select>
                </div>
            </div>
        </div> -->

        <!-- spécifique aux objectifs --->
        <div v-if="type === 'lens'" class="space-y-4">
            <div>
                <label class="text-sm text-grain">Monture</label>
                <select 
                    v-model="form.mount"
                    class="w-full p-3 rounded-lg bg-white border border-gray-200"
                >
                    <option disabled value="">Sélectionnez une monture</option>
                    <option 
                        v-for="mount in mountStore.mounts" 
                        :key="mount.id" 
                        :value="mount.id"
                    >
                        {{ mount.name }}
                    </option>
                </select>
            </div>

            <div>
                <label class="text-sm text-grain">Compatible avec</label>
                <select 
                    v-model="form.cameras_ids" 
                    multiple
                    class="w-full p-3 rounded-lg bg-white border border-gray-200"
                >
                    <option 
                        v-for="camera in cameraStore.cameras" 
                        :key="camera.id" 
                        :value="camera.id"
                    >
                        {{ camera.model }}
                    </option>
                </select>
                <p class="text-xs text-grain mt-1">
                    Maintenez la touche Ctrl (ou Cmd sur Mac) pour sélectionner plusieurs caméras.
                </p>
            </div>
        </div>

        <!-- Champ commun : Description -->
        <div>
            <label class="text-sm text-grain">Description</label>
            <textarea 
                v-model="form.description" 
                rows="3"
                class="w-full p-3 rounded-lg bg-white border border-gray-200 resize-none"
            ></textarea>
        </div>

        <p v-if="error" class="text-sm text-danger">{{ error }}</p>
        
        <BaseButton block type="submit">
            {{ submitLabel }}
        </BaseButton>
    </form>

</template>