<script setup>
    import { ref, computed } from 'vue'

    import { useRoute } from 'vue-router'
    const route = useRoute()
    const isRegister = computed(()=> route.path === "/register")

    const username = ref("")
    const email = ref("")
    const password1 = ref("")
    const password2 = ref("")
    const role = ref("")

    async function login() {
        const resp = await fetch("http://localhost:3000/login", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({
                                username: username.value,
                                password: password1.value
                            })

        })
        const data = await resp.json()
        const token = data.authorization_token
        alert(token)
    }

    async function register() {
        if (password1.value!=password2.value) {
            alert("Passwords do not match!")
            return
        }
        const resp = await fetch("http://localhost:3000/register", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({
                                username: username.value,
                                email: email.value,
                                password: password1.value,
                                role: role.value
                            })
        })
        alert("Successfully registered.")
    }
</script>

<template>
    
    <form @submit.prevent="isRegister ? register() : login()">
        <fieldset>
            <legend v-if="isRegister">Register</legend>
            <legend v-else>Login</legend>
            <label for="username">Username</label>
            <input id="username" type="text" v-model="username" /><br>
            <label for="email" v-if="isRegister">Email</label>
            <input id="email" type="email" v-model="email" v-if="isRegister"/><br>
            <label for="role" v-if="isRegister">Role</label>
            <select id="role" v-model="role" v-if="isRegister">
                <option value="admin">Admin</option>
                <option value="company">Company</option>
                <option value="student">Student</option>
            </select><br>

            <label for="password1">Password</label>
            <input id="password1" type="password" v-model="password1" /><br>
            <label for="password2" v-if="isRegister">Enter password again</label>
            <input id="password2" type="password" v-model="password2" v-if="isRegister"/><br>
        
            <button type="submit">Submit</button>
            <RouterLink to="/login" v-if="isRegister">Login instead</RouterLink>
            <RouterLink to="/register" v-else>If you don't have an account, register</RouterLink> 
        </fieldset>
    </form>
</template>

<style scoped>
    form {
       
    }
</style>
