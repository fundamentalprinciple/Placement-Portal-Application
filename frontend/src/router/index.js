import { createRouter, createWebHistory } from 'vue-router'

import Auth from '@/features/auth/Auth.vue'
import About from '@/features/about/About.vue'
import Dashboard from '@/features/dashboard/Dashboard.vue'

const routes = [
    { path: '/', component: Dashboard },
    { path: '/login', component: Auth },
    { path: '/register', component: Auth },
    { path: '/about', component: About },

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
