<script setup>
    import { ref } from 'vue';
    //import  { router } from 'vue-router';   

    const name = ref("")
    const username = ref("")
    const gender = ref("")
    const email = ref("")
    const degree = ref("")
    const cgpa = ref("")
    const year = ref("")
    const password1 = ref("")
    const password2 = ref("")

    const role = "student";

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
                gender: gender.value,
                email: email.value,
                role: role,
                degree: degree.value,
                cgpa: parseFloat(cgpa.value),
                year: year.value,
                password: password1.value
            })
        });
        const data = await response.json();
        alert(`Account registered successfully, you can login now, your username is ${data['username']}`);
        this.$router.push("/login");
    }

</script>

<template>
    <form @submit.prevent="register()">
        <fieldset>
            <legend>Student Register</legend>
            <label for="name">Name</label>
            <input v-model="name" id="name" name="name" type="text" required />
            <br />

            <label for="gender">Gender</label>
            <select v-model="gender" id="gender" name="gender" type="text" required >
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Trans">Trans</option>
            </select>
            <br />

            <label for="username">Username</label>
            <input v-model="username" id="username" name="username" type="text" required />
            <br />

            <label for="email">Email</label>
            <input v-model="email" id="email" name="email" type="email" required />
            <br />

            <label for="degree">Major</label>
            <select v-model="degree" id="degree" name="degree" required >
                <option value="Computer Engineering">Computer Engineering</option>
                <option value="Computer Science Engineering">Computer Science Engineering</option>
                <option value="Electrical Engineering">Electrical Engineering</option>
                <option value="Mechanical Engineering">Mechanical Engineering</option>
                <option value="Civil Engineering">Civil Engineering</option>
                <option value="Chemical Engineering">Chemical Engineering</option>
                <option value="Aerospace Engineering">Aerospace Engineering</option>
                <option value="Automotive Engineering">Automotive Engineering</option>
                <option value="Robotics Engineering">Robotics Engineering</option>
                <option value="Nanotechnology Engineering">Nanotechnology Engineering</option>
                <option value="Data Science and Applications">Data Science and Applications</option>
                <option value="Electronic Systems">Electronic Systems</option>
                <option value="Management and Data Science">Management and Data Science</option>
            </select>
            <br />
            
            <label for="cgpa">CGPA</label>
            <input v-model="cgpa" id="cgpa" name="cgpa" type="range" min="0" max="10" step="0.01" oninput="valueDisplay.textContent = this.value"/>
            <span id="valueDisplay">5</span>
            
            <br />

            <label for="year">Year of graduation</label>
            <select v-model="year" id="year" name="year" required >
                <option value="2021">2021</option>
                <option value="2022">2022</option>
                <option value="2023">2023</option>
                <option value="2024">2024</option>
                <option value="2025">2025</option>
                <option value="2026">2026</option>
            </select>
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
