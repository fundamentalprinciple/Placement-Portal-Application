<script setup>
    import { ref, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { useAuthStore } from '@/stores/auth'

    const router = useRouter()
    const auth = useAuthStore()
    const profile = ref({})
    const editing = ref(false)
    const form = ref({
        name: '',
        degree: '',
        cgpa: '',
        year: ''
    })
    const loading = ref(false)
    const message = ref('')

    onMounted(async () => {
        await fetchProfile()
    })

    async function fetchProfile() {
        try {
            const response = await fetch('http://localhost:3000/api/self-manage-student-profile', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': auth.token
                }
            })
            if (!response.ok) throw new Error('Failed to fetch profile')
            profile.value = await response.json()
            form.value = { ...profile.value }
        } catch (err) {
            message.value = 'Error loading profile.'
            console.error(err)
        }
    }

    async function saveProfile() {
        loading.value = true
        message.value = ''
        try {
            const response = await fetch('http://localhost:3000/api/self-manage-student-profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': auth.token
                },
                body: JSON.stringify(form.value)
            })
            const data = await response.json()
            if (!response.ok) throw new Error(data.message || 'Failed to update profile')
            message.value = data.message
            editing.value = false
            await fetchProfile()  // Refresh profile
        } catch (err) {
            message.value = err.message
        } finally {
            loading.value = false
        }
    }

    function startEditing() {
        editing.value = true
        message.value = ''
    }

    function cancelEditing() {
        editing.value = false
        form.value = { ...profile.value }
        message.value = ''
    }
</script>

<template>
    <div class="profile-container">
        <h2>Student Profile</h2>
        
        <div v-if="!editing">
            <div class="profile-info">
                <p><strong>Name:</strong> {{ profile.name }}</p>
                <p><strong>Degree:</strong> {{ profile.degree }}</p>
                <p><strong>CGPA:</strong> {{ profile.cgpa }}</p>
                <p><strong>Year:</strong> {{ profile.year }}</p>
            </div>
            <button @click="startEditing" class="edit-btn">Edit Profile</button>
        </div>
        
        <div v-else>
            <form @submit.prevent="saveProfile" class="edit-form">
                <label>Name</label>
                <input v-model="form.name" type="text" required />
                
                <label>Degree</label>
                <input v-model="form.degree" type="text" required />
                
                <label>CGPA</label>
                <input v-model="form.cgpa" type="number" step="0.01" min="0" max="10" required />
                
                <label>Year</label>
                <select v-model="form.year" required>
                    <option value="2021">2021</option>
                    <option value="2022">2022</option>
                    <option value="2023">2023</option>
                    <option value="2024">2024</option>
                    <option value="2025">2025</option>
                    <option value="2026">2026</option>
                </select>
                
                <div class="form-actions">
                    <button type="submit" :disabled="loading" class="save-btn">
                        {{ loading ? 'Saving...' : 'Save Changes' }}
                    </button>
                    <button type="button" @click="cancelEditing" class="cancel-btn">Cancel</button>
                </div>
            </form>
        </div>
        
        <div v-if="message" class="message">{{ message }}</div>
        
        <button @click="router.push('/')" class="back-btn">Back to Dashboard</button>
    </div>
</template>

<style scoped>
    .profile-container {
        max-width: 500px;
        margin: 30px auto;
        padding: 30px;
        border: 1px solid lightblue;
        border-radius: 10px;
        background-color: #ECEBFA;
        box-shadow: 10px 10px 5px rgba(173, 188, 255, 0.35);
    }
    
    .profile-info p {
        margin: 10px 0;
        font-family: "Montserrat", sans-serif;
    }
    
    .edit-form {
        display: flex;
        flex-direction: column;
    }
    
    label {
        margin-top: 15px;
        font-family: "Montserrat", sans-serif;
    }
    
    input, select {
        padding: 10px;
        border: 1px solid lightblue;
        border-radius: 8px;
        font-family: "Montserrat", sans-serif;
    }
    
    .form-actions {
        margin-top: 20px;
        display: flex;
        gap: 10px;
    }
    
    .edit-btn, .save-btn, .cancel-btn, .back-btn {
        background-color: lightblue;
        border: none;
        border-radius: 8px;
        padding: 10px 15px;
        font-family: "Montserrat", sans-serif;
        cursor: pointer;
        margin-top: 10px;
    }
    
    .edit-btn:hover, .save-btn:hover, .back-btn:hover {
        background-color: #9FBFF0;
    }
    
    .cancel-btn:hover {
        background-color: #FFAB91;
    }
    
    .message {
        margin-top: 15px;
        padding: 10px;
        border-radius: 8px;
        font-family: "Montserrat", sans-serif;
        background-color: #E8F5E8;
        color: green;
    }
</style>
