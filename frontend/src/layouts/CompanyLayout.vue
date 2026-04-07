<script setup>
    import { useRouter } from 'vue-router'
    import Hello from '@/components/Hello.vue'
    import CompanyApplicationSearch from '@/features/company/CompanyApplicationSearch.vue'
    import CreateDrive from '@/features/company/CreateDrive.vue'
    import ViewDrives from '@/features/company/ViewDrives.vue'
    import ManageApplications from '@/features/company/ManageApplications.vue'
    import ComapnyInterview from '@/features/company/CompanyInterviews.vue'

    const router = useRouter()
</script>

<template>
    <Hello />
    <div class="button-bar">
        <CompanyApplicationSearch />
        <button @click="router.push('/company/profile')" class="profile-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
            </svg>
            Profile
        </button>
    </div>
    <div class="controls">
        <CreateDrive />
        <ViewDrives />
        <ManageApplications />
        <ComapnyInterview />
    </div>
</template>

<style scoped>
    .button-bar {
        text-align: center;
        margin: 20px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }
    
    .profile-btn {
        background-color: lightblue;
        border: none;
        border-radius: 8px;
        padding: 10px 15px;
        font-family: "Montserrat", sans-serif;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        box-shadow: 5px 5px 5px rgba(173, 188, 255, 0.35);
    }
    
    .profile-btn:hover {
        background-color: #9FBFF0;
    }
    
    .controls {
        margin-left: 10vw;
        margin-right: 10vw;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-around;
    }
    
    .controls > * {
        margin-top: 30px;
    }
</style>
