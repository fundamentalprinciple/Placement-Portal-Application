<script setup>
    import { ref } from 'vue';
    import { useAuthStore } from '@/stores/auth'

    const auth = useAuthStore()

    const job_title = ref("")
    const job_description = ref("")
    const deadline = ref("")

    const degree = ref("") 
    const cgpa = ref(5)
    const year = ref("")


    async function createDrive() {
        const response = await fetch("http://localhost:3000/api/create-drive", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": auth.token
            },
            body: JSON.stringify({
                job_title: job_title.value,
                job_description: job_description.value,
                eligibility_criteria: `["${degree.value}",${cgpa.value},${year.value}]`,
                deadline: deadline.value,
            })
        });
        document.getElementById("form").reset();
    }
    
</script>

<template>
    <form id="form" @submit.prevent="createDrive()">
        <fieldset>
            <legend>Create Drive</legend>
            <div class="group">
                <label for="job_title">Job Title</label><br>
                <input v-model="job_title" id="job_title" name="job_title" type="text" required />
            </div>

            <div class="group">
                <label for="job_description">Job Description</label><br>
                <textarea style="padding: 20px; height: 200px; width: 400px; border: 1px solid lightblue; border-radius: 20px;" v-model="job_description" id="job_description" name="job_description" type="text" required />

            </div>

            <div class="group">
                <label for="deadline">Deadline</label>
                <input style="width:150px; margin-left: 20px;" v-model="deadline" id="deadline" name="deadline" type="date" required />
            </div>

            <div class="criteria">
                <p>Eligbility Criteria</p><br>

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
                <br />
                <br />
                <label for="cgpa">Minimum CGPA</label><br>
                <input style="width: 300px;" v-model="cgpa" id="cgpa" name="cgpa" type="range" min="0" max="10" step="0.01" oninput="valueDisplay.textContent = this.value"/>
                <div style="font-size: x-large;" id="valueDisplay">5</div>
                <br />
                <br />
                <label for="year">Minimum Year of graduation</label>
                <select v-model="year" id="year" name="year" required >
                    <option value="2021">2021</option>
                    <option value="2022">2022</option>
                    <option value="2023">2023</option>
                    <option value="2024">2024</option>
                    <option value="2025">2025</option>
                    <option value="2026">2026</option>
                </select>
            </div>
            <button type="submit">Submit</button>
        </fieldset>
    </form>    
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    form {
        border: 1px solid lightblue;
        border-radius: 20px;
        padding: 30px;
        min-width: 500px;
        width: 550px;
        margin: auto;
        margin-bottom: 10vh;
        background-color: #ECEBFA;
        box-shadow: 10px 10px 5px lightblue;
    }

    legend {
        font-family: "Bebas Neue", sans-serif;
        font-size: xx-large;
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
        background-color: lightblue;
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

    .criteria {
        margin: 20px auto 20px auto;
        border: 1px solid lightblue;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 5px 5px 5px lightblue;
    }

    legend {
        padding-left: 30%;
    }

    p {
        margin-top: 20px;
        text-align: center;
    }
</style>
