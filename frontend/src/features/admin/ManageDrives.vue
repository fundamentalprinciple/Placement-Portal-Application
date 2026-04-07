<script setup>
    import { ref, onMounted } from 'vue'
    import { useAuthStore } from '@/stores/auth'
    import { useDriveStore } from '@/stores/drives'

    const auth = useAuthStore()
    const driveStore = useDriveStore()

    const new_status = ref('approved')

    let eligibility_criteria = ref([]);


    onMounted(async() => {
        await driveStore.fetchAllDrives()
    })

    async function changeStatus(id, status) {
        await driveStore.changeDriveStatus(id, status);
        await driveStore.fetchAllDrives()
    }


</script>

<template>
    <div class="container">
        <h2>Placement Drives</h2>
        <div v-for="drive in driveStore.drives" class="profile">
            <h4>{{ drive.job_title }}</h4>
            <p style="color:green;" v-if="drive.status=='approved'"><strong>Approval Status:</strong>       Approved</p>
            <p style="color:blue;" v-if="drive.status=='pending'"><strong>Approval Status:</strong>       Pending</p>
            <p style="color:red;" v-if="drive.status=='closed'"><strong>Approval Status:</strong>       Closed</p>
            <p><strong>Job Description:</strong> <br>           {{ drive.job_description }}</p>
            <p><strong>Company:</strong>           {{ drive.company_name }}</p>

            <p><strong>Eligibility Criteria:</strong></p>
            <p>Major: <br>
                {{
                    (() => {
                        const criteria = JSON.parse(drive.eligibility_criteria)
                        return Array.isArray(criteria[0]) ? criteria[0].join(', ') : criteria[0]
                    })()
                }}
            </p>
            <p>Min. CGPA: <br>{{JSON.parse(drive.eligibility_criteria)[1]}}</p>
            <p>Min. Year of Graduation: <br>{{JSON.parse(drive.eligibility_criteria)[2]}}</p>

            <p><strong>Deadline:</strong> <br>           {{ drive.deadline }}</p>

            <p><strong>Set Status:</strong></p>
            <select v-model="new_status" >
                <option value="approved">Approve</option>
                <option value="closed">Close</option>
            </select>
            <button @click="changeStatus(drive.id,new_status)">Set</button>

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
        margin-bottom: 50px;
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
        margin-left: 40px;
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
