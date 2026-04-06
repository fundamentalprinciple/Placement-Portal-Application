<script setup>
    import { useRouter } from 'vue-router'
    import Hello from '@/components/Hello.vue'
    import ApplyDrive from '@/features/student/ApplyDrive.vue'
    import AppliedDrives from '@/features/student/AppliedDrives.vue'    
    import StudentInterviews from '@/features/student/StudentInterviews.vue'

    const router = useRouter()
</script>

<template>
    <Hello />
    <div class="profile-btn-container">
        <button @click="router.push('/student/profile')" class="profile-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
            </svg>
            Profile
        </button>
    </div>
    <div class="controls">
        <ApplyDrive />
        <AppliedDrives />
        <StudentInterviews />
    </div>
</template>

<style scoped>
   .profile-btn-container {
        text-align: center;
        margin: 20px 0;
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
    }
    
    .profile-btn:hover {
        background-color: #9FBFF0;
    }
    
    .controls {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    } 
       
</style>
