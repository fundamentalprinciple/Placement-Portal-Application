import { createRouter, createWebHistory } from 'vue-router'

import MainLayout from '@/layouts/MainLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: MainLayout },
    { path: '/login', component: MainLayout },
    { path: '/register-student', component: MainLayout },
    { path: '/register-company', component: MainLayout },
    { path: '/logout', component: MainLayout },
    { path: '/about', component: MainLayout }
    ]
})

export default router
