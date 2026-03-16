import { defineStore } from "pinia";
import api from "@/api/axios";

export const useMountStore = defineStore("mounts", {
    state: () => ({
        mounts: [],
    }),

    actions: {
        async fetchMounts() {
            const response = await api.get("mounts/");
            this.mounts = response.data.results;
        }
    }
})