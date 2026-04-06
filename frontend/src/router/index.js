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
    { path: '/about', component: MainLayout },
    { path: '/admin/student-profile/:id', component: MainLayout },
    { path: '/admin/company-profile/:id', component: MainLayout },
    { path: '/company/profile', component: MainLayout },
    { path: '/student/profile', component: MainLayout }
    ]
})

export default router
