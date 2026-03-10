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
            return response.data;
        },

        async createCamera(data) {
            const response = await api.post("cameras/", data);

            // on recharge la liste des cameras pour inclure la nouvelle camera
            await this.fetchCameras();
            
            return response.data;
        },

        async updateCamera(id, data) {
            const response = await api.put(`cameras/${id}/`, data);

            // on recharge la liste des cameras pour inclure les modifications
            await this.fetchCameras();
            
            return response.data;
        },
        
        async deleteCamera(id) {
            await api.delete(`cameras/${id}/`);
            this.cameras = this.cameras.filter(camera => camera.id !== id);
            
            // on recharge la liste des cameras pour retirer la camera supprimée
            await this.fetchCameras();
        }
    }
})