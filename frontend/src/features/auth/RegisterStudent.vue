<script setup>
    import { ref } from 'vue';
    import  { useRouter } from 'vue-router';   

    const router = useRouter()

    const name = ref("")
    const username = ref("")
    const gender = ref("")
    const email = ref("")
    const degree = ref("")
    const cgpa = ref(5)
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
        router.push("/login");
        document.getElementById("form").reset();
        alert(`Account registered successfully, you can login now, your username: ${data['user']['username']}.`);
    }

</script>

<template>
    <form id="form" @submit.prevent="register()">
        <fieldset>
            <legend>Student Register</legend>
            <div class="group">
                <label for="name">Name</label><br>
                <input v-model="name" id="name" name="name" type="text" required />
            </div>

            <div class="group">
                <label for="gender">Gender</label><br>
                <select v-model="gender" id="gender" name="gender" type="text" required >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Trans">Trans</option>
                </select>

            <div class="group">
                <label for="username">Set a Username</label><br>
                <input v-model="username" id="username" name="username" type="text" required />
            </div>

            <div class="group">
                <label for="email">Email</label><br>
                <input v-model="email" id="email" name="email" type="email" required />
            </div>

            <div class="group">
                <label for="degree">Major</label><br>
                <select style="width:250px" v-model="degree" id="degree" name="degree" required >
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
            </div>
            
            <div class="group">
                <label for="cgpa">CGPA</label><br>
                <input style="width: 300px;" v-model="cgpa" id="cgpa" name="cgpa" type="range" min="0" max="10" step="0.01" oninput="valueDisplay.textContent = this.value"/>
                <div style="font-size: x-large; color: white;" id="valueDisplay">5</div>
            </div>

            <div class="group">
                <label for="year">Year of graduation</label></div>
                <select v-model="year" id="year" name="year" required >
                    <option value="2021">2021</option>
                    <option value="2022">2022</option>
                    <option value="2023">2023</option>
                    <option value="2024">2024</option>
                    <option value="2025">2025</option>
                    <option value="2026">2026</option>
                </select>
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

    input, select {
        padding: 10px;
        height: 35px;
        width: 400px;
        border: none;
        border-radius: 10px;
    }
    
    select {
        padding: 5px;
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
