import { defineStore } from "pinia"
import api from "@/api/axios"

export const useAuthStore = defineStore("auth", {
    state: () => ({
        user: null,
        access: localStorage.getItem("access_token") || null,
        refresh: localStorage.getItem("refresh_token") || null,
    }),

    actions: {
        async login(username, password) {
            const response = await api.post("token/", {
                username,
                password,
            })

            this.access = response.data.access
            this.refresh = response.data.refresh

            localStorage.setItem("access_token", this.access)
            localStorage.setItem("refresh_token", this.refresh)

            await this.fetchUser()
        },

        async fetchUser() {
            const response = await api.get("me/")
            this.user = response.data
        },

        logout() {
            this.user = null
            this.access = null
            this.refresh = null

            localStorage.removeItem("access_token")
            localStorage.removeItem("refresh_token")
        },
    },

})