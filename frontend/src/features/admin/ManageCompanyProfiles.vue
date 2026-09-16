<script setup>
import { API_BASE_URL } from '@/config/api'
    import { ref } from 'vue'
    import { useAuthStore } from '@/stores/auth'

    const auth = useAuthStore()
    const new_status = ref('approved')

    let companyList = ref([]);

    async function getCompanyProfiles() {
        const response = await fetch(`${API_BASE_URL}/api/manage-company-profiles`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": auth.token
            },
        })

        companyList.value = await response.json()
    }

    getCompanyProfiles()

    async function changeAccountStatus(id,new_status) {
        const response = await fetch(`${API_BASE_URL}/api/manage-company-profiles`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": auth.token
            },
            body: JSON.stringify({
                id: id,
                new_status: new_status
            })
        })
        await getCompanyProfiles();
    }

    async function approveProfileChanges(id) {
        const response = await fetch(`${API_BASE_URL}/api/manage-company-profiles`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": auth.token
            },
            body: JSON.stringify({
                id: id,
                action: 'approve_profile'
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
            <p style="color:green;" v-if="company.approval_status=='approved'"><strong>Approval Status:</strong> Approved</p>
            <p style="color:blue;" v-if="company.approval_status=='pending'"><strong>Approval Status:</strong> Pending</p>
            <p style="color:red;" v-if="company.approval_status=='rejected'"><strong>Approval Status:</strong> Rejected</p>
            <p><strong>HR Contact:</strong> {{ company.hr_contact }}</p>
            <p><strong>Email:</strong> {{ company.email }}</p>
            <p><strong>Website:</strong> {{ company.website }}</p>
            
            <div v-if="company.pending_name || company.pending_hr_contact || company.pending_website" class="pending-section">
                <h5>Pending Profile Changes</h5>
                <p v-if="company.pending_name"><strong>New Name:</strong> {{ company.pending_name }}</p>
                <p v-if="company.pending_hr_contact"><strong>New HR Contact:</strong> {{ company.pending_hr_contact }}</p>
                <p v-if="company.pending_website"><strong>New Website:</strong> {{ company.pending_website }}</p>
                <button @click="approveProfileChanges(company.id)">Approve Changes</button>
            </div>
            
            <select v-model="new_status">
                <option value="approved">Approve</option>
                <option value="pending">Set Pending</option>
                <option value="rejected">Reject</option>
            </select>
            <button @click="changeAccountStatus(company.id, new_status)">Update Status</button>
        </div>
    </div>
</template>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    h1, h2, h4, h5 {
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

    .pending-section {
        margin-top: 15px;
        padding: 10px;
        border: 1px solid orange;
        border-radius: 8px;
        background-color: #FFF8E1;
    }

    .pending-section h5 {
        margin-top: 0;
        color: orange;
    }

    button {
        background-color: lightblue;
        border: none;
        border-radius: 10px;
        padding: 8px 12px;
        margin: 5px;
        cursor: pointer;
    }

    button:hover {
        background-color: #E3D888;
    }

    select {
        border: 1px solid lightblue;
        border-radius: 10px;
        height: 35px;
        width: 120px;
        margin-right: 10px;
    }

</style>
