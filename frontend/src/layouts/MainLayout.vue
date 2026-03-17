<script setup>
    import { ref, inject} from 'vue'
    import { useRoute } from 'vue-router'

    import AuthLayout from '@/layouts/AuthLayout.vue'
    import AdminLayout from '@/layouts/AdminLayout.vue'
    import CompanyLayout from '@/layouts/CompanyLayout.vue'
    import StudentLayout from '@/layouts/StudentLayout.vue'
    import NotAuthenticated from '@/layouts/NotAuthenticated.vue'

    const route = useRoute()   
    const authenticated = inject('authenticated')
    const role = inject('role')

</script>

<template>
    <AuthLayout v-if="['/login', '/register-student', '/register-company', '/logout'].includes(route.path)"/>
    
    <AdminLayout v-else-if="authenticated && role=='admin'" />
    <CompanyLayout v-else-if="authenticated && role=='company'" />
    <StudentLayout v-else-if="authenticated && role=='student'"  />
    <NotAuthenticated v-else />

</template>

<style scoped></style>
