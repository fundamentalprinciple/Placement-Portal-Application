<script setup>
    import { useRoute } from 'vue-router'

    import Login from '@/features/auth/Login.vue'
    import RegisterStudent from '@/features/auth/RegisterStudent.vue'
    import RegisterCompany from '@/features/auth/RegisterCompany.vue'
    import Logout from '@/features/auth/Logout.vue'
        
    const route = useRoute()

</script>

<template>
    <Login v-if="route.path == '/login'"/>

    <RegisterStudent v-if="route.path === '/register-student'" />
    
    <RegisterCompany v-if="route.path === '/register-company'" />

    <Logout v-if="route.path == '/logout'"/>
    
</template>

<style>
</style>
