<script setup>
    import { ref } from 'vue'
    import { useRoute } from 'vue-router'

    import AuthLayout from '@/layouts/AuthLayout.vue'
    //import AdminLayout from '@/layouts/AdminLayout'
    //import CompanyLayout from '@/layouts/CompanyLayout'
    //import StudentLayout from '@/layouts/StudentLayout'

    const route = useRoute()       
</script>

<template>
    <AuthLayout v-if="route.path == '/login' || route.path == '/register-student' || route.path=='/register-company'"/>
    
</template>

<style scoped></style>
