<script setup>
import { API_BASE_URL } from '@/config/api'
    import { ref } from 'vue';
    import  { useRouter } from 'vue-router';
    import { useAuthStore } from '@/stores/auth';

    const auth = useAuthStore()
    const router = useRouter()

    const name = ref("")
    const hr_contact = ref("")
    const website = ref("")
    const username = ref("")
    const email = ref("")
    const password1 = ref("")
    const password2 = ref("")

    const role = "company";
    
    async function register() {
        if(password1.value!=password2.value) {
            alert("Passwords do not match!")
            return
        }

        if(auth.isAuthenticated) {
            auth.logout()
        }

        const response = await fetch(`${API_BASE_URL}/api/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name.value,
                username: username.value,
                email: email.value,
                role: role,
                hr_contact: hr_contact.value,
                website: website.value,
                password: password1.value
            })
        });
        const data = await response.json();
        router.push("/login");
        document.getElementById("form").reset();
        alert(`Applied for registeration successfully, awaiting admin approval.`);
    }

</script>

<template>
    <form id="form" @submit.prevent="register()">
        <fieldset>
            <legend>Company Register</legend>
            <div class="group">
                <label for="name">Name</label><br>
                <input v-model="name" id="name" name="name" type="text" required />
            </div>

            <div class="group">
                <label for="username">Username</label><br>
                <input v-model="username" id="username" name="username" type="text" required />
            </div>

            <div class="group">
                <label for="email">Email</label><br>
                <input v-model="email" id="email" name="email" type="email" required />
            </div>

            <div class="group">
                <label for="hr_contact">HR Contact</label><br>
                <input v-model="hr_contact" id="hr_contact" name="hr_contact" type="tel" pattern="[0-9]{10}" placeholder="+91"/>
            </div>

            <div class="group">
                <label for="website">Website</label><br>
                <input v-model="website" id="website" name="website" type="text" placeholder="example.com"/>
            </div>

            <div class="group">
                <label for="password1">Set Password</label><br>
                <input v-model="password1" id="password1" name="password1" type="password" required />
            </div>

            <div class="group">
                <label for="password2">Confirm Password</label><br>
                <input v-model="password2" id="password2" name="password2" type="password" required />
            </div>

            <button type="submit">Submit</button>
            <p>If you already have an account, <RouterLink class="link" to="/login">login</RouterLink></p>
        </fieldset>
    </form>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    form {
        border: none;
        border-radius: 20px;
        padding: 30px;
        min-width: 500px;
        width: 550px;
        margin: auto;
        margin-top: 10vh;
        margin-bottom: 10vh;
        background-color: #773344;
    }

    legend, label, p {
        color: white;
    }

    legend {
        font-family: "Bebas Neue", sans-serif;
    }

    label, p {
        font-family: "Montserrat", sans-serif;
    }

    fieldset {
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    input, select {
        padding: 10px;
        height: 35px;
        width: 400px;
        border: none;
        border-radius: 10px;
    }

    select {
        width: 100px;
    }

    button {
        border: none;
        border-radius: 10px;
        font-weight: bold;
        height: 40px;
        width: 100px;
        margin: auto;
        margin-bottom: 20px;
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
        padding-left: 30%;
    }

    p {
        margin-top: 20px;
        text-align: center;
    }

</style>
