<script setup>
    import { ref } from 'vue'
    import { useAuthStore } from '@/stores/auth'
    import { useRoute } from 'vue-router'

    import AuthLayout from '@/layouts/AuthLayout.vue'
    import AdminLayout from '@/layouts/AdminLayout.vue'
    import CompanyLayout from '@/layouts/CompanyLayout.vue'
    import StudentLayout from '@/layouts/StudentLayout.vue'
    import NotAuthenticated from '@/layouts/NotAuthenticated.vue'

    import About from '@/components/About.vue'

    import AdminStudentProfile from '@/features/admin/AdminStudentProfile.vue'
    import AdminCompanyProfile from '@/features/admin/AdminCompanyProfile.vue'
    import CompanyProfile from '@/features/company/CompanyProfile.vue'
    import StudentProfile from '@/features/student/StudentProfile.vue'
    import CompanyStudentProfile from '@/features/company/CompanyStudentProfile.vue'
    import StudentHistory from '@/features/student/StudentHistory.vue'

    const route = useRoute()   
    const auth = useAuthStore()

</script>

<template>
    <AuthLayout v-if="['/login', '/register-student', '/register-company', '/logout'].includes(route.path)"/>
    <About v-else-if="route.path === '/about'" />
    <AdminStudentProfile v-else-if="auth.isAuthenticated && auth.role == 'admin' && route.path.startsWith('/admin/student-profile')" />
    <AdminCompanyProfile v-else-if="auth.isAuthenticated && auth.role == 'admin' && route.path.startsWith('/admin/company-profile')" />    
    <CompanyProfile v-else-if="auth.isAuthenticated && auth.role=='company' && route.path=='/company/profile'" />
    <StudentProfile v-else-if="auth.isAuthenticated && auth.role=='student' && route.path=='/student/profile'" />
    <CompanyStudentProfile v-else-if="auth.isAuthenticated && auth.role=='company' && route.path.startsWith('/company/student-profile')" />
    <StudentHistory v-else-if="auth.isAuthenticated && auth.role == 'student' && route.path.startsWith('/student/history')" />
    <AdminLayout v-else-if="auth.isAuthenticated && auth.role=='admin'" />
    <CompanyLayout v-else-if="auth.isAuthenticated && auth.role=='company'" />
    <StudentLayout v-else-if="auth.isAuthenticated && auth.role=='student'"  />
    <NotAuthenticated v-else />

</template>

<style scoped></style>
