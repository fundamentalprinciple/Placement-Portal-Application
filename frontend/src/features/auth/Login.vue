<script setup>
    import { ref } from "vue"
    import { useAuthStore } from '@/stores/auth'
    import  { useRouter } from 'vue-router';   
 
    const router = useRouter()

    const username = ref("")
    const password = ref("")

    async function login() {
        try {

            if (!username.value || !password.value) {
                alert("Username and password are required.");
                return;
            }
            
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

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                alert(errorData.message || "Login failed. Please check your credentials or try again later.");
                return;
            }

            const data = await response.json();
            const token = data['auth_token']
            if (!token) {
                alert("Authentication token not received. Please try again.");
                return;
            }
                const auth = useAuthStore()
                auth.login({ token, username: username.value })
                await auth.authenticate()
            router.push("/");
        } catch (err) {
            alert("An unexpected error occurred. Please try again.");
        }
    }


</script>

<template>
    <form @submit.prevent="login()">
        <fieldset>
            <legend>Login</legend>
            <div class="group">
                <label for="username">Username</label><br>
                <input v-model="username" id="username" name="username" type="text" required />
            </div>
            
            <div class="group">
                <label for="password">Password</label><br>
                <input v-model="password" id="password" name="password" type="password" required />
            </div>            

            <button type="submit">Submit</button>
            <br />
            <p>If you don't have an account, register as a <RouterLink class="link" to="/register-student">Student</RouterLink> or <RouterLink class="link" to="/register-company">Company</RouterLink></p>
        </fieldset>
    </form>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    form {
        border: none;
        border-radius: 20px;
        padding: 30px;
        min-width: 400px;
        width: 400px;
        margin: auto;
        margin-top: 10vh;
        margin-bottom: 10vh;
        background-color: #773344;
    }

    legend, label, p {
        color: white;
    }

    legend {
        font-family: "Bebar Neue", sans-serif;
    }  

    label, p {
        font-family: "Montserrat", sans-serif;
    }  

    fieldset {
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    input {
        padding: 10px; 
        height: 35px;
        width: 300px;
        border: none;
        border-radius: 10px;
    }

    button {
        border: none;
        border-radius: 10px;
        font-weight: bold;
        height: 40px;
        width: 100px;
        margin: auto;
    }    

    button:hover {
        background-color: #E3D888;
    }
    
   .link {
        text-decoration: none;
        color: #40E0D0;
    }

    .link:hover {
        color: #E3D888;
    } 

    .group {
        margin: 20px auto 20px auto;
    }
    
    legend {
        padding-left: 40%;
    }

    p {
        text-align: center;
        margin: auto;
    }

</style>
