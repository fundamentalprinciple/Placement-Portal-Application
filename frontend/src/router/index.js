import { createRouter, createMemoryHistory } from 'vue-router'

import Auth from '../components/Auth.vue'
import About from '../components/About.vue'

const routes = [
    { path: '/login', component: Auth },
    { path: '/register', component: Auth },
    { path: '/about', component: About },

]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router
