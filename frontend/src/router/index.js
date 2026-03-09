import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import LoginView from "@/views/LoginView.vue"
import DashboardView from "@/views/DashboardView.vue"
import RollsView from "@/views/RollsView.vue"
import RollDetailView from "@/views/RollDetailView.vue"
import RollCreateView from "@/views/RollCreateView.vue"
import CamerasView from "@/views/CamerasView.vue"
import CameraDetailView from "@/views/CameraDetailView.vue"
import CameraCreateView from "@/views/CameraCreateView.vue"
import LensesView from "@/views/LensesView.vue"
import LensDetailView from "@/views/LensDetailView.vue"
import LensCreateView from "@/views/LensCreateView.vue"

const routes = [
  { path: "/login", component: LoginView },
  { path: "/", component: DashboardView, meta: { requiresAuth: true } },
  { path: "/rolls", component: RollsView, meta: { requiresAuth: true } },
  { path: "/rolls/new", component: RollCreateView, meta: { requiresAuth: true } },
  { path: "/rolls/:slug", component: RollDetailView, meta: { requiresAuth: true } },
  { path: "/cameras", component: CamerasView, meta: { requiresAuth: true } },
  { path: "/cameras/new", component: CameraCreateView, meta: { requiresAuth: true } },
  { path: "/cameras/:id", component: CameraDetailView, meta: { requiresAuth: true } },
  { path: "/lenses", component: LensesView, meta: { requiresAuth: true } },
  { path: "/lenses/new", component: LensCreateView, meta: { requiresAuth: true } },
  { path: "/lenses/:id", component: LensDetailView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.access) {
    return "/login"
  }
})

export default router
