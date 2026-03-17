<script setup>
    import { ref, inject } from 'vue'

    const token = localStorage.getItem('Authentication-Token')
    const new_status = ref('approved')

    let companyList = ref([]);

    async function getCompanyProfiles() {
        const response = await fetch("http://localhost:3000/api/manage-company-profiles", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": token
            },
        })

        companyList.value = await response.json()
    }

    getCompanyProfiles()

    async function changeAccountStatus(id,new_status) {
        const response = await fetch("http://localhost:3000/api/manage-company-profiles", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": token
            },
            body: JSON.stringify({
                id: id,
                new_status: new_status
            })
        })
        await getCompanyProfiles();
    }

</script>

<template>
    <div class="container">
        <h2>Company Profiles</h2>
        <div v-for="company in companyList" class="profile">
            <h4>{{ company.name }}</h4>
            <p style="color:green;" v-if="company.approval_status=='approved'"><strong>Approval Status:</strong>       Approved</p>
            <p style="color:blue;" v-if="company.approval_status=='pending'"><strong>Approval Status:</strong>       Pending</p>
            <p style="color:red;" v-if="company.approval_status=='rejected'"><strong>Approval Status:</strong>       Rejected</p>
            <p><strong>HR Contact:</strong>           {{ company.hr_contact }}</p>
            <p><strong>Email:</strong>           {{ company.email }}</p>
            <p><strong>Website:</strong>            {{ company.website }}</p>

            <p><strong>Set Status:</strong></p>
            <select v-model="new_status" >
                <option value="approved">Approve</option>
                <option value="rejected">Reject</option>
            </select>
            <button @click="changeAccountStatus(company.id,new_status)">Set</button>

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
