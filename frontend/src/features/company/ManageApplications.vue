<script setup>
    import { ref, onMounted } from 'vue'
    import { useAuthStore } from '@/stores/auth'
    import { useDriveStore } from '@/stores/drives'
    import ScheduleInterview from '@/features/company/ScheduleInterview.vue'    

    const auth = useAuthStore()
    const driveStore = useDriveStore()

    let new_status = ref("")

    onMounted(async()=>{
        try{
            await driveStore.fetchApplicationsByCompany()
        } catch(err) {
            console.error("error")
        }
    })

    async function update(id, new_status) {
        await driveStore.updateApplicationStatus(id,new_status)
        await driveStore.fetchApplicationsByCompany()
    }
</script>

<template>
    <div class="container">
        <h2>Applications</h2>
        <div v-if="driveStore.loading === false" v-for="app in driveStore.applications" class="profile">
            <h4>{{ app.job_title }}</h4>
            <p><strong>Student:</strong> <br>           {{ app.student_name }}</p>

            <p v-if="app.student_qualifications">
                <strong>Qualifications:</strong><br>
                <span v-if="(parsed = JSON.parse(app.student_qualifications))">
                    Major: {{ parsed[0] }} <br>
                    CGPA: {{ parsed[1] }} <br>
                    Year: {{ parsed[2] }}
                </span>
            </p>

            <p><strong>Application Date:</strong> <br> {{ app.application_date }}</p>
            <p style="color:green;" v-if="app.status=='selected'"><strong>Status:</strong>       Selected</p>
            <p style="color:orange;" v-if="app.status=='shortlisted'"><strong>Status:</strong>       Shortlisted</p>
            <p style="color:red;" v-if="app.status=='rejected'"><strong>Status:</strong>       Not Qualified</p>
            <p style="color:blue;" v-if="app.status=='applied'"><strong>Status:</strong>       Applied</p> 

            <p><strong>Set Status:</strong></p>
            <select v-model="new_status" >
                <option value="shortlisted">Shortlist</option>
                <option value="selected">Select</option>
                <option value="rejected">Reject</option>
            </select><br>
 
            <button @click="update(app.id, new_status)">Set</button>
            
            <ScheduleInterview :application="app" />

        </div>
    </div>
</template>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    h1, h2, h4 {
        font-family: "Bebas Neue", sans-serif;
        text-align: center;
    }

    p, button {
        font-family: "Montserrat", sans-serif;
    }


    .container {
        border: 1px solid lightblue;
        border-radius: 10px;
        background-color: #ECEBFA;
        width: 400px;
        padding-top: 50px;
        padding-bottom: 50px;
        box-shadow: 10px 10px 5px lightblue;
    }

    .profile {
        padding: 20px;
        margin: auto;
        margin-bottom: 20px;
        border: 1px solid lightblue;
        border-radius: 10px;
        width: 300px;
        box-shadow: 5px 5px 5px lightblue;
    }

    button {
        background-color: lightblue;
        border: none;
        border-radius: 10px;
        padding: 10px;
        margin: auto;
        width: 60px;
    }

    button:hover {
        background-color: #E3D888;
    }

    select {
        border: 1px solid lightblue;
        border-radius: 10px;
        height: 40px;
        width: 150px;
    }
</style>
