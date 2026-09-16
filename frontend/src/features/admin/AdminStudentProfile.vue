<script setup>
import { API_BASE_URL } from '@/config/api'
    import { ref, onMounted } from 'vue'
    import { useRouter, useRoute } from 'vue-router'
    import { useAuthStore } from '@/stores/auth'

    const router = useRouter()
    const route = useRoute()
    const auth = useAuthStore()
    const student = ref(null)
    const error = ref('')

    onMounted(async () => {
        try {
            const id = route.params.id
            const response = await fetch(`${API_BASE_URL}/api/student-profile/${id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': auth.token
                }
            })

            if (!response.ok) throw new Error('Failed to fetch student profile')
            student.value = await response.json()
        } catch (err) {
            error.value = err.message
        }
    })

    function goBack() {
        router.push('/')
    }

    async function downloadResume() {
    const response = await fetch(`${API_BASE_URL}/api/student-resume/${student.value.id}`, {
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
    a.download = student.value.resume_filename
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
}

</script>

<template>
    <div class="profile-page">
        <button @click="goBack" class="back-btn">← Back to Dashboard</button>
        <div v-if="error" class="error">{{ error }}</div>
        <div v-else-if="student" class="profile-container">
            <h1>{{ student.name }}</h1>
            <div class="profile-details">
                <p><strong>Gender:</strong> {{ student.gender }}</p>
                <p><strong>Degree:</strong> {{ student.degree }}</p>
                <p><strong>CGPA:</strong> {{ student.cgpa }}</p>
                <p><strong>Year:</strong> {{ student.year }}</p>
                <p><strong>Available:</strong> {{ student.available ? 'Yes' : 'No' }}</p>
                <p><strong>Account Status:</strong> {{ student.account_status ? 'Active' : 'Inactive' }}</p>
            </div>
            <div v-if="student.resume_filename" class="resume-row">
                <strong>Resume:</strong>
                <button @click="downloadResume" class="download-btn" style="margin-left: 10px;">
                    Download Resume
                </button>
            </div>
            <p v-else><strong>Resume:</strong> Not uploaded</p>
        </div>
    </div>
</template>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    .profile-page {
        padding: 30px;
        max-width: 800px;
        margin: 50px auto;
    }

    .back-btn, .download-btn {
        background-color: lightblue;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-family: "Montserrat", sans-serif;
        cursor: pointer;
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
        margin: 50px auto;
        width: 500px;
    }

    h1 {
        font-family: "Bebas Neue", sans-serif;
        margin-bottom: 30px;
    }

    .profile-details {
        font-family: "Montserrat", sans-serif;
    }

    .profile-details p {
        padding: 12px 0;
        border-bottom: 1px solid lightblue;
    }

    .profile-details p:last-child {
        border-bottom: none;
    }

    .loading, .error {
        font-family: "Montserrat", sans-serif;
        padding: 30px;
        text-align: center;
    }

    .error {
        color: #d32f2f;
    }
</style>
