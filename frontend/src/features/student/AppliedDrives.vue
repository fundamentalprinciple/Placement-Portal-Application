<script setup>
    import { ref, onMounted, computed } from 'vue'
    import { useAuthStore } from '@/stores/auth'
    import { useDriveStore } from '@/stores/drives'

    const auth = useAuthStore()
    const driveStore = useDriveStore()

    const new_status = ref('approved')

    let eligibility_criteria = ref([]);


    onMounted(async() => {
        await driveStore.fetchAppliedDrives()
    })

    async function deleteApp(id) {
        await driveStore.deleteApplication(id);
        await driveStore.fetchAppliedDrives()
    }


</script>

<template>
    <div class="container">
        <h2>Applied Drives</h2>
        <div v-for="app in driveStore.applications" class="profile">
            <h4>{{ app.job_title }}</h4>
            <p><strong>Job Description:</strong> <br>           {{ app.job_description }}</p>
            <p><strong>Company:</strong> <br>           {{ app.company_name }}</p>
            <p><strong>Application Date:</strong> <br> {{ app.application_date }}</p>
            <p style="color:green;" v-if="app.status=='selected'"><strong>Status:</strong>       Selected</p>
            <p style="color:yellow;" v-if="app.status=='shortlisted'"><strong>Status:</strong>       Shortlisted</p>
            <p style="color:red;" v-if="app.status=='rejected'"><strong>Status:</strong>       Not Qualified</p>
            <p style="color:blue;" v-if="app.status=='applied'"><strong>Status:</strong>       Applied</p> 

            <button @click="deleteApp(app.id)">Withdraw</button>

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
        width: 550px;
        padding-top: 50px;
        padding-bottom: 50px;
        box-shadow: 10px 10px 5px lightblue;
        margin-bottom: 50px;
    }

    .profile {
        padding: 20px;
        margin: auto;
        margin-bottom: 20px;
        border: 1px solid lightblue;
        border-radius: 10px;
        width: 400px;
        box-shadow: 5px 5px 5px lightblue;
    }

    button {
        background-color: lightblue;
        border: none;
        border-radius: 10px;
        padding: 10px;
        margin-left: 36%;
        width: 100px;
    }

    button:hover {
        background-color: red;
        color: white;
    }

    select {
        border: 1px solid lightblue;
        border-radius: 10px;
        height: 40px;
        width: 150px;
    }
</style>
