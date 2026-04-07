<script setup>
    import { ref, onMounted } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    import { useAuthStore } from '@/stores/auth'

    const route = useRoute()
    const router = useRouter()
    const auth = useAuthStore()
    const profile = ref(null)
    const error = ref('')

    async function loadProfile() {
        const id = route.params.id
        const response = await fetch(`http://localhost:3000/api/student-profile/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': auth.token
            }
        })
        if (!response.ok) {
            error.value = 'Failed to load student profile.'
            return
        }
        profile.value = await response.json()
    }

    async function downloadResume() {
        if (!profile.value || !profile.value.resume_filename) return
        const response = await fetch(`http://localhost:3000/api/student-resume/${profile.value.id}`, {
            method: 'GET',
            headers: {
                'Authentication-Token': auth.token
            }
        })
        if (!response.ok) return
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = profile.value.resume_filename
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
    }

    function goBack() {
        router.push('/')
    }

    onMounted(loadProfile)
</script>

<template>
    <div class="profile-container">
        <div class="profile-card" v-if="profile">
            <h2>{{ profile.name }}</h2>
            <p><strong>Gender:</strong> {{ profile.gender }}</p>
            <p><strong>Degree:</strong> {{ profile.degree }}</p>
            <p><strong>CGPA:</strong> {{ profile.cgpa }}</p>
            <p><strong>Year:</strong> {{ profile.year }}</p>
            <p><strong>Available:</strong> {{ profile.available ? 'Yes' : 'No' }}</p>
            <div v-if="profile.resume_filename" class="resume-row">
                <strong>Resume:</strong>
                <button @click="downloadResume" class="download-btn">
                    Download Resume
                </button>
            </div>
            <p v-else><strong>Resume:</strong> Not uploaded</p>
         <button class="back-btn" @click="goBack">Back to dashboard</button>
        </div>

        <div class="profile-card error" v-else>
            {{ error || 'Loading profile...' }}
        </div>
    </div>
</template>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    .back-btn {
        background-color: lightblue;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-family: "Montserrat", sans-serif;
        cursor: pointer;
        margin-top: 10px;
    }

    .back-btn:hover {
        background-color: #9FBFF0;
    }

    .profile-container {
        background-color: #ECEBFA;
        border: 1px solid lightblue;
        border-radius: 10px;
        padding: 40px;
        box-shadow: 10px 10px 5px rgba(173, 188, 255, 0.35);
        max-width:500px;
        margin: 50px auto;
    }

    h1 {
        font-family: "Bebas Neue", sans-serif;
        margin-bottom: 30px;
    }

    .profile-card {
        font-family: "Montserrat", sans-serif;
    }

    .profile-card p {
        padding: 12px 0;
        border-bottom: 1px solid lightblue;
    }

    .profile-details p:last-child {
        border-bottom: none;
    }


    .resume-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 12px;
    }

    .download-btn {
        background-color: lightblue;
        border: none;
        border-radius: 8px;
        padding: 8px 12px;
        cursor: pointer;
        font-family: "Montserrat", sans-serif;
    }

    .download-btn:hover {
        background-color: #9FBFF0;
    }
</style>
