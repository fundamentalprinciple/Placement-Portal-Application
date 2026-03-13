<script setup>
</script>

<template>
    <form>
        <fieldset>
            <legend>Student Register</legend>
            <label for="name">Name</label>
            <input v-model="name" id="name" name="name" type="text" required />
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
                <option value="Data Science and Appications">Data Science and Appications</option>
                <option value="Electronic Systems">Electronic Systems</option>
                <option value="Management and Data Science">Management and Data Science</option>
            </select>
            <br />
            
            <label for="cgpa">CGPA</label>
            <input v-model="cgpa" id="cgpa" name="cgpa" type="range" min="0" max="50" />
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
            <p v-if="route.path == '/login'">If you don't have an account, <RouterLink to="/register">register</RouterLink></p>
        </fieldset>
    </form>
</template>

<style scoped>
</style>
