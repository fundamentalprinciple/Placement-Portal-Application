<script setup>
    import { ref, onMounted, computed } from 'vue'
    import { useAuthStore } from '@/stores/auth'
    import { useDriveStore } from '@/stores/drives'

    const auth = useAuthStore()
    const driveStore = useDriveStore()

    const new_status = ref('approved')

    let eligibility_criteria = ref([]);


    onMounted(async() => {
        await driveStore.fetchAllDrives()
    })

    const approvedDrives = computed(() => {
        return driveStore.drives.filter(
            drive => drive.status === 'approved'
        )
    })
    
    async function apply(id) {
        await driveStore.applyDrive(id);
        await driveStore.fetchAllDrives()
    }


</script>

<template>
    <div class="container">
        <h2>Ongoing Drives</h2>
        <div v-for="drive in approvedDrives" class="profile">
            <h4>{{ drive.job_title }}</h4>
            <p><strong>Job Description:</strong> <br>           {{ drive.job_description }}</p>
            <p><strong>Company:</strong>           {{ drive.company_name }}</p>

            <p><strong>Eligibility Criteria:</strong></p>
            <p>Major: <br>{{JSON.parse(drive.eligibility_criteria)[0]}}</p>
            <p>Min. CGPA: <br>{{JSON.parse(drive.eligibility_criteria)[1]}}</p>
            <p>Min. Year of Graduation: <br>{{JSON.parse(drive.eligibility_criteria)[2]}}</p>

            <p><strong>Deadline:</strong> <br>           {{ drive.deadline }}</p>

            <button @click="apply(drive.id)">Apply</button>

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
        background-color: #E3D888;
    }

    select {
        border: 1px solid lightblue;
        border-radius: 10px;
        height: 40px;
        width: 150px;
    }
</style>
