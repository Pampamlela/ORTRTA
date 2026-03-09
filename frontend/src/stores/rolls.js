import { defineStore } from "pinia"
import api from "@/api/axios"

export const useRollStore = defineStore("rolls", {
    state: () => ({
        stats: null,
        rolls: [],
        currentRoll: null,
    }),

    actions: {

        async fetchStats() {
            const response = await api.get("stats/");
            this.stats = response.data;
        },

        async fetchRolls() {
            const response = await api.get("rolls/");
            this.rolls = response.data.results;
        },

        async fetchRoll(slug) {
            const response = await api.get(`rolls/${slug}/`);
            this.currentRoll = response.data;
        },

        async createRoll(data) {
            const response = await api.post("rolls/", data);

            // on recharge la liste des rolls pour inclure le nouveau roll
            await this.fetchRolls();
            
            return response.data;
        }
    }
})