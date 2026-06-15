import axios  from "axios"
import { ref } from "vue" 
import router from "@/router"
import { useAuthStore } from "@/stores/auth"

export const apiError = ref(null)

// on attache automatiquement le token d'authentification à chaque requête sortante, si il existe dans le localStorage.
const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api/"
})

api.interceptors.request.use(config => {
    const token = localStorage.getItem("access")
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// interceptor pour gérer les erreurs de réponse de l'API
api.interceptors.response.use(
    response => response,
    error => {
        const authStore = useAuthStore()
        if (error.response && error.response.status === 401) {
            authStore.logout()
            router.push("/login")
        } else if (!error.response){ 
                apiError.value = "Le serveur ne répond pas. Veuillez réessayer plus tard."
        } 
        
        return Promise.reject(error)
    }
)

export default api