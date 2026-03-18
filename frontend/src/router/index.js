import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import LoginView from "@/views/LoginView.vue"
import RegisterView from "@/views/RegisterView.vue"
import DashboardView from "@/views/DashboardView.vue"
import RollsView from "@/views/RollsView.vue"
import RollDetailView from "@/views/RollDetailView.vue"
import RollCreateView from "@/views/RollCreateView.vue"
import RollEditView from "@/views/RollEditView.vue"
import CamerasView from "@/views/CamerasView.vue"
import CameraDetailView from "@/views/CameraDetailView.vue"
import CameraCreateView from "@/views/CameraCreateView.vue"
import CameraEditView from "@/views/CameraEditView.vue"
import LensesView from "@/views/LensesView.vue"
import LensDetailView from "@/views/LensDetailView.vue"
import LensCreateView from "@/views/LensCreateView.vue"
import LensEditView from "@/views/LensEditView.vue"
import ProfileView from "@/views/ProfileView.vue"


const routes = [
  { path: "/login", component: LoginView, meta: { guestOnly: true } },
  { path: "/register", component: RegisterView },
  { path: "/", component: DashboardView, meta: { requiresAuth: true } },
  { path: "/profile", component: ProfileView, meta: { requiresAuth: true } },
  { path: "/rolls", component: RollsView, meta: { requiresAuth: true } },
  { path: "/rolls/new", component: RollCreateView, meta: { requiresAuth: true } },
  { path: "/rolls/:slug", component: RollDetailView, meta: { requiresAuth: true } },
  { path: "/rolls/:slug/edit", component: RollEditView, meta: { requiresAuth: true } },
  { path: "/cameras", component: CamerasView, meta: { requiresAuth: true } },
  { path: "/cameras/new", component: CameraCreateView, meta: { requiresAuth: true } },
  { path: "/cameras/:id", component: CameraDetailView, meta: { requiresAuth: true } },
  { path: "/cameras/:id/edit", component: CameraEditView, meta: { requiresAuth: true } },
  { path: "/lenses", component: LensesView, meta: { requiresAuth: true } },
  { path: "/lenses/new", component: LensCreateView, meta: { requiresAuth: true } },
  { path: "/lenses/:id", component: LensDetailView, meta: { requiresAuth: true } },
  { path: "/lenses/:id/edit", component: LensEditView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.accessToken) {
    next("/login")

  } 

  else if (to.meta.guestOnly && authStore.accessToken) {
    next("/rolls")
  } 

  else {
    next()
  }
})

export default router
