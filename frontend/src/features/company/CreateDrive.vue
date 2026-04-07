<script setup>
    import { ref } from 'vue';
    import { useAuthStore } from '@/stores/auth'
    import { useDriveStore } from '@/stores/drives'

    import DegreeMultiSelect from '@/components/DegreeMultiSelect.vue'

    const auth = useAuthStore()
    const driveStore = useDriveStore()

    const job_title = ref("")
    const job_description = ref("")
    const deadline = ref("")

    const degree = ref([]) 
    const cgpa = ref(5)
    const year = ref("")

    async function createDrive() {
        await driveStore.createDrive({
            job_title: job_title.value,
            job_description: job_description.value,
            eligibility_criteria: JSON.stringify([degree.value, parseFloat(cgpa.value), year.value]),
            deadline: deadline.value,
        })
        document.getElementById('form').reset()
        await driveStore.fetchDrivesByCompany()
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
                
                <label for="degree">Majors</label><br>
                <DegreeMultiSelect v-model="degree" />

                <br />
                <br />
                <label for="cgpa">Minimum CGPA</label><br>
                <input
                    style="width: 300px;"
                    v-model.number="cgpa"
                    id="cgpa"
                    name="cgpa"
                    type="number"
                    min="0.00"
                    max="10.00"
                    step="0.01"
                    required
                />
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
        width: 550px;
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
        height: 50px;
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
