<script setup>
    import { ref } from "vue"
    import  { useRouter } from 'vue-router';   
 
    const router = useRouter()

    const username = ref("")
    const password = ref("")

    async function login() {
        alert("login function called")
        const response = await fetch('http://localhost:3000/api/login', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                    username: username.value,
                    password: password.value
            })    
        });
        
        const data  = await response.json();
        localStorage.setItem("Authentication-Token", data['auth_token']);
        router.push("/");
        alert('You logged in successfully!');
    }


</script>

<template>
    <form @submit.prevent="login()">
        <fieldset>
            <legend>Login</legend>
            <label for="username">Username</label>
            <input v-model="username" id="username" name="username" type="text" required />
            <br />
            <label for="password">Password</label>
            <input v-model="password" id="password" name="password" type="password" required />
            <br />
            <button type="submit">Submit</button>
            <br />
            <p>If you don't have an account, register as a <RouterLink to="/register-student">Student</RouterLink> or <RouterLink to="/register-company">Company</RouterLink></p>
        </fieldset>
    </form>
</template>

<style scoped>
</style>
