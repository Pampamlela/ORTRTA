import { defineStore } from "pinia";
import api from "@/api/axios";

export const useLensStore = defineStore("lenses", {
    state: () => ({
        lenses: [],
        currentLens: null,
    }),

    actions: {
        async fetchLenses() {
            const response = await api.get("lenses/");
            this.lenses = response.data.results;
        },

        async fetchLens(id) {
            const response = await api.get(`lenses/${id}/`);
            this.currentLens = response.data;
            return response.data;
        },

        async createLens(data) {
            const response = await api.post("lenses/", data);

            // on recharge la liste des lenses pour inclure la nouvelle lens
            await this.fetchLenses();

            return response.data;
        },

        async updateLens(id, data) {
            const response = await api.put(`lenses/${id}/`, data);

            // on recharge la liste des lenses pour inclure les modifications
            await this.fetchLenses();

            return response.data;
        },

        async deleteLens(id) {
            await api.delete(`lenses/${id}/`);
            this.lenses = this.lenses.filter(lens => lens.id !== id);
            
            // on recharge la liste des lenses pour retirer la lens supprimée
            await this.fetchLenses();
        },
    }
})
