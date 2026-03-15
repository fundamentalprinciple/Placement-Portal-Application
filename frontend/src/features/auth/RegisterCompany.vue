<script setup>
    import { ref } from 'vue';
    import  { useRouter } from 'vue-router';

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
        const response = await fetch("http://localhost:3000/api/register", {
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
        alert(`Applied for registeration successfully, awaiting admin approval.}.`);
    }

</script>

<template>
    <form id="form" @submit.prevent="register()">
        <fieldset>
            <legend>Company Register</legend>
            <label for="name">Name</label>
            <input v-model="name" id="name" name="name" type="text" required />
            <br />

            <label for="username">Username</label>
            <input v-model="username" id="username" name="username" type="text" required />
            <br />

            <label for="email">Email</label>
            <input v-model="email" id="email" name="email" type="email" required />
            <br />

            <label for="hr_contact">HR Contact</label>
            <input v-model="hr_contact" id="hr_contact" name="hr_contact" type="tel" pattern="[0-9]{10}" placeholder="+91"/>
            <br />

            <label for="website">Website</label>
            <input v-model="website" id="website" name="website" type="text" placeholder="example.com"/>
            <br />

            <label for="password1">Set Password</label>
            <input v-model="password1" id="password1" name="password1" type="password" required />
            <br />

            <label for="password2">Confirm Password</label>
            <input v-model="password2" id="password2" name="password2" type="password" required />
            <br />

            <button type="submit">Submit</button>
            <br />
            <p>If you already have an account, <RouterLink to="/login">login</RouterLink></p>
        </fieldset>
    </form>
</template>

<style scoped>
</style>
