import { defineStore } from "pinia";
import api from "@/api/axios";

export const useCameraStore = defineStore("cameras", {
    state: () => ({
        cameras: [],
        currentCamera: null,
    }),

    actions: {
        async fetchCameras() {
            const response = await api.get("cameras/");
            this.cameras = response.data.results;
        },

        async fetchCamera(id) {
            const response = await api.get(`cameras/${id}/`);
            this.currentCamera = response.data;
        },

        async createCamera(data) {
            const response = await api.post("cameras/", data);

            // on recharge la liste des cameras pour inclure la nouvelle camera
            await this.fetchCameras();
            
            return response.data;
        },
    }
})