<script setup>
    import { ref, onMounted, computed } from 'vue'
    import { useAuthStore } from '@/stores/auth'
    import { useDriveStore } from '@/stores/drives'

    const auth = useAuthStore()
    const driveStore = useDriveStore()

    const new_status = ref('approved')
    let recruitmentRequests = ref([])

    let eligibility_criteria = ref([]);


    onMounted(async() => {
        await driveStore.fetchAppliedDrives()
        await getRecruitmentRequests()
    })

    async function deleteApp(id) {
        await driveStore.deleteApplication(id);
        await driveStore.fetchAppliedDrives()
    }

    async function getRecruitmentRequests() {
        const response = await fetch("http://localhost:3000/api/manage-recruitment-request", {
            method: "GET",
            headers: {
                "Authentication-Token": auth.token
            }
        })
        if (response.ok) {
            const allRequests = await response.json()
            recruitmentRequests.value = allRequests.filter(req => req.status === 'pending')
            await driveStore.fetchAppliedDrives()
        }
    }

    async function respondRecruitment(request_id, action) {
        const response = await fetch("http://localhost:3000/api/manage-recruitment-request", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": auth.token
            },
            body: JSON.stringify({
                request_id,
                action
            })
        })
    
        if (response.ok) {
            alert(`Recruitment request ${action}ed`)
            await getRecruitmentRequests()
            await driveStore.fetchAppliedDrives()
        } else {
            const error = await response.json()
            alert(`Error: ${error.message}`)
        }
    }


</script>

<template>
    <div class="container">

        <div v-if="recruitmentRequests.length > 0" style="margin-bottom: 30px;">
            <h2 style="text-align: center; margin-bottom: 20px;">Recruitment Notifications</h2>
            <div v-for="req in recruitmentRequests" :key="req.id" class="recruitment-card">
                <p style="color: #4CAF50; font-weight: bold; font-size: 18px;">
                    You have been recruited: {{ req.company_name }}
                </p>
                <p><strong>Position:</strong> {{ req.job_title }}</p>
                <p><strong>Received:</strong> {{ req.created_date }}</p>
                
                <button 
                    @click="respondRecruitment(req.id, 'confirm')"
                    style="background-color: #4CAF50; color: white; margin-right: 10px;"
                >
                    Confirm
                </button>
                <button 
                    @click="respondRecruitment(req.id, 'cancel')"
                    style="background-color: #f44336; color: white;"
                >
                    Cancel
                </button>
            </div>
        </div>
        

        <h2>Your Applications</h2>
            <div v-for="app in driveStore.applications" :key="app.id" class="profile">
                <h4>{{ app.job_title }}</h4>
                <p><strong>Job Description:</strong> <br>           {{ app.job_description }}</p>
                <p><strong>Company:</strong> <br>           {{ app.company_name }}</p>
                <p><strong>Application Date:</strong> <br> {{ app.application_date }}</p>
                <p style="color:green;" v-if="app.status=='selected'"><strong>Status:</strong>       Selected</p>
                <p style="color:orange;" v-if="app.status=='shortlisted'"><strong>Status:</strong>       Shortlisted</p>
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

    .profile, .recruitment-card {
        padding: 20px;
        margin: auto;
        margin-bottom: 20px;
        border: 1px solid lightblue;
        border-radius: 10px;
        width: 400px;
        box-shadow: 5px 5px 5px lightblue;
    }

    .recruitment-card {
        background-color: #f0f8f0;
        border: 2px solid #4CAF50;
    }

    button {
        background-color: lightblue;
        border: none;
        border-radius: 10px;
        padding: 10px;
        margin-left: 36%;
        width: 100px;
        margin-bottom: 10px;
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
