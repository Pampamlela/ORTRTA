import { defineStore } from "pinia"

export const useToastStore = defineStore("toast", {
  state: () => ({
    toasts: []
  }),
  actions: {
    addToast(message, type = "success") {
        const id = Date.now()
        this.toasts.push({ id, message, type })
        // disparition automatique du toast après 3 secondes
        setTimeout(() => this.removeToast(id), 3000)
    },
    removeToast(id) {
      this.toasts = this.toasts.filter(t => t.id !== id)
    }
  }
})