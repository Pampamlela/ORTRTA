import { defineStore } from "pinia"
import api from "@/api/axios"

export const useAuthStore = defineStore("auth", {
    state: () => ({
        user: null,
        access: localStorage.getItem("access_token") || null,
        refresh: localStorage.getItem("refresh_token") || null,
    }),

    actions: {

        async register(data) {
            const response = await api.post("register/", data)

            this.user = response.data.user
            this.accessToken = response.data.access
            this.refreshToken = response.data.refresh

            localStorage.setItem("access", this.accessToken)
            localStorage.setItem("refresh", this.refreshToken)
        },

        async login(data) {
            const response = await api.post("login/", data)

            this.accessToken = response.data.access
            this.refreshToken = response.data.refresh

            localStorage.setItem("access", this.accessToken)
            localStorage.setItem("refresh", this.refreshToken)

            await this.fetchMe()
        },

        async fetchUser() {
            const response = await api.get("me/")
            this.user = response.data
        },

        logout() {
            this.user = null
            this.accessToken = null
            this.refreshToken = null

            localStorage.removeItem("access")
            localStorage.removeItem("refresh")
        },
    },

})