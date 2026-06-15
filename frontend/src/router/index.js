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
import RGPDView from "@/views/RGPDView.vue"
import NotFoundView from "@/views/NotFoundView.vue"


const routes = [
  { path: "/login", name: "login", component: LoginView, meta: { guestOnly: true } },
  { path: "/register", name: "register", component: RegisterView },
  { path: "/rgpd", name: "rgpd", component: RGPDView },
  { path: "/", name: "dashboard", component: DashboardView, meta: { requiresAuth: true } },
  { path: "/profile", name: "profile", component: ProfileView, meta: { requiresAuth: true } },
  { path: "/rolls", name: "rolls", component: RollsView, meta: { requiresAuth: true } },
  { path: "/rolls/new", name: "roll-create", component: RollCreateView, meta: { requiresAuth: true } },
  { path: "/rolls/:slug", name: "roll-detail", component: RollDetailView, meta: { requiresAuth: true } },
  { path: "/rolls/:slug/edit", name: "roll-edit", component: RollEditView, meta: { requiresAuth: true } },
  { path: "/cameras", name: "cameras", component: CamerasView, meta: { requiresAuth: true } },
  { path: "/cameras/new", name: "camera-create", component: CameraCreateView, meta: { requiresAuth: true } },
  { path: "/cameras/:id", name: "camera-detail", component: CameraDetailView, meta: { requiresAuth: true } },
  { path: "/cameras/:id/edit", name: "camera-edit", component: CameraEditView, meta: { requiresAuth: true } },
  { path: "/lenses", name: "lenses", component: LensesView, meta: { requiresAuth: true } },
  { path: "/lenses/new", name: "lens-create", component: LensCreateView, meta: { requiresAuth: true } },
  { path: "/lenses/:id", name: "lens-detail", component: LensDetailView, meta: { requiresAuth: true } },
  { path: "/lenses/:id/edit", name: "lens-edit",   component: LensEditView, meta: { requiresAuth: true } },
  { path: "/:pathMatch(.*)*", name: "not-found", component: NotFoundView },
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
