<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCameraStore } from '@/stores/cameras';
import { useLensStore } from '@/stores/lenses';
import PageContainer from '@/components/PageContainer.vue';
import BaseButton from '@/components/BaseButton.vue';

const router = useRouter();
const cameraStore = useCameraStore();
const lensStore = useLensStore();

onMounted(() => {
    cameraStore.fetchCameras();
    lensStore.fetchLenses();
})
</script>

<template>
    <PageContainer>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
             
            <!-- Liste des appareils photo -->
            <div>
                <h2 class="font-title text-xl mb-4 text-film">Appareils photo</h2>

                <div class="bg-white rounded-lg p-6 min-h-48">
                    <p class="text-sm text-grain mb-4">Modèles</p>

                    <div v-if="cameraStore.cameras.length ===0" class="text-sm text-grain">
                        Aucun appareil photo pour le moment.
                    </div>

                    <ul v-else class="space-y-2">
                        <li v-for="camera in cameraStore.cameras" :key="camera.id">
                            <router-link
                                :to="`/cameras/${camera.id}/edit`"
                                class="hover:text-amber"
                            >
                                {{ camera.model }}
                            </router-link>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Liste des objectifs -->
            <div>
                <div class="flex justify-between items-center mb-4">
                    <h2 class="font-title text-xl text-film">Objectifs</h2>
                </div>

                <div class="bg-white rounded-lg p-6 min-h-48">
                    <p class="text-sm text-grain mb-4">Modèles</p>

                    <div v-if="lensStore.lenses.length ===0" class="text-sm text-grain">
                        Aucun objectif pour le moment.
                    </div>

                    <ul v-else class="space-y-2">
                        <li v-for="lens in lensStore.lenses" :key="lens.id">
                            <router-link
                                :to="`/lenses/${lens.id}/edit`"
                                class="hover:text-amber"
                            >
                                {{ lens.model }}
                            </router-link>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </PageContainer>
</template>
