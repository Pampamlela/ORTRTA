import { defineStore } from "pinia";
import api from "@/api/axios";

export const useCameraStore = defineStore("cameras", {
    state: () => ({
        cameras: [],
    }),

    actions: {
        async fetchCameras() {
            const response = await api.get("cameras/");
            this.cameras = response.data.results;
        }
    }
})