<script setup>
    import { ref, onMounted, provide } from 'vue'
    import { useRoute } from 'vue-router'

    import AuthLayout from '@/layouts/AuthLayout.vue'
    import AdminLayout from '@/layouts/AdminLayout.vue'
    import CompanyLayout from '@/layouts/CompanyLayout.vue'
    import StudentLayout from '@/layouts/StudentLayout.vue'
    import NotAuthenticated from '@/layouts/NotAuthenticated.vue'

    const route = useRoute()       

    const name = ref("")
    const role = ref("")
    const authenticated = ref(false)

    async function authenticate() {
        if (localStorage.getItem('username') && localStorage.getItem('Authentication-Token')) {
            const username = localStorage.getItem('username')

            const response = await fetch("http://localhost:3000/api/authenticate", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": localStorage.getItem('Authentication-Token')
                },
                body: JSON.stringify({
                    username: localStorage.getItem('username') 
                })
            })

            const authData = await response.json()
        
            name.value = authData.name
            role.value = authData.role
            authenticated.value = true
        }
    }

    onMounted(()=>{
        authenticate()
    })

    provide("authenticated", authenticated)
    provide("name", name)
    provide("role", role)

</script>

<template>
    <AuthLayout v-if="route.path == '/login' || route.path == '/register-student' || route.path=='/register-company' || route.path == '/logout'"/>
    
    <AdminLayout v-else-if="role=='admin'" />
    <CompanyLayout v-else-if="role=='company'" />
    <StudentLayout v-else-if="role=='student'"  />
    <NotAuthenticated v-else-if="authenticated==false" />

</template>

<style scoped></style>
