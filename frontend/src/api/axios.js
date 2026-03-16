import axios  from "axios"

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

export default api