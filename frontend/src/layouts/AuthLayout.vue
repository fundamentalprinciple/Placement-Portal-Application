<script setup>
    import { useRoute } from 'vue-router'

    import Login from '@/features/auth/Login.vue'
    import RegisterStudent from '@/features/auth/RegisterStudent.vue'
    import RegisterCompany from '@/features/auth/RegisterCompany.vue'
        
    const route = useRoute()

</script>

<template>
    <Login v-if="route.path == '/login'"/>

    <RegisterStudent v-if="route.path === '/register-student'" />
    
    <RegisterCompany v-if="route.path === '/register-company'" />
    
</template>

<style>
</style>
