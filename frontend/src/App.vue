<script setup>
    import { ref, onMounted, provide, watch } from 'vue'
    import { useRoute } from 'vue-router'
    import Navbar from '@/components/Navbar.vue'
    
    const route = useRoute()

    const name = ref("")
    const role = ref("")
    let authenticated = ref(false)

    const token = ref(localStorage.getItem('Authentication-Token'))
    const username = ref(localStorage.getItem('username'))
    
    async function authenticate() {
        token.value = localStorage.getItem('Authentication-Token');
        username.value = localStorage.getItem('username');
        if (username.value && token.value) {
            try {
                const response = await fetch("http://localhost:3000/api/authenticate", {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": token.value
                    },
                    body: JSON.stringify({
                        username: username.value
                    })
                })

                if (!response.ok) throw new Error()

                const authData = await response.json()
                name.value = authData.name
                role.value = authData.role
                authenticated.value = true
            } catch (err) {
                authenticated.value = false
                role.value = ""
                name.value = ""
            }
        } else {
            authenticated.value = false
        }
    }

    onMounted(()=>{
        authenticate()
    })

    provide("authenticated", authenticated)
    provide("name", name)
    provide("role", role)

    watch(()=> route.path, ()=>{
        authenticate()
    })

    watch([token, username], () => {
        authenticate()
    })

</script>

<template>
    <Navbar />
    <main>
        <RouterView /> 
    </main>
</template>

<style scoped>
</style>
