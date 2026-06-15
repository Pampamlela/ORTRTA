import { defineStore } from "pinia"
import api from "@/api/axios"

export const useRollStore = defineStore("rolls", {
    state: () => ({
        stats: null,
        rolls: [],
        currentRoll: null,
        count: 0, // nombre total de rolls (pour la pagination)
        next: null, // URL de la page suivante (pour la pagination)
        previous: null, // URL de la page précédente (pour la pagination)
    }),

    actions: {

        async fetchStats() {
            const response = await api.get("stats/");
            this.stats = response.data;
        },

        async fetchRolls(url = null) {
            const endpoint = url || "rolls/?ordering=-date_start";
            const response = await api.get(endpoint);
            this.rolls = response.data.results;
            this.count = response.data.count;
            this.next = response.data.next;
            this.previous = response.data.previous;
        },

        async fetchRoll(slug) {
            const response = await api.get(`rolls/${slug}/`);
            this.currentRoll = response.data;
            return response.data;
        },

        async createRoll(data) {
            const response = await api.post("rolls/", data);

            // on recharge la liste des rolls pour inclure le nouveau roll
            await this.fetchRolls();
            
            return response.data;
        },

        async updateRoll(slug, data) {
            const response = await api.put(`rolls/${slug}/`, data);
            return response.data
        },

        async deleteRoll(slug) {
            await api.delete(`rolls/${slug}/`);

            // on recharge la liste des rolls pour retirer le roll supprimé
            await this.fetchRolls();
        },

    }
})