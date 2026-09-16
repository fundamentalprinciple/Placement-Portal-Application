<script setup>
import { API_BASE_URL } from '@/config/api'
    import { ref, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { useAuthStore } from '@/stores/auth'

    const router = useRouter()
    const auth = useAuthStore()
    const profile = ref({})
    const editing = ref(false)
    const form = ref({
        name: '',
        hr_contact: '',
        website: ''
    })
    const loading = ref(false)
    const message = ref('')

    onMounted(async () => {
        await fetchProfile()
    })

    async function fetchProfile() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/company-profile`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': auth.token
                }
            })
            if (!response.ok) throw new Error('Failed to fetch profile')
            profile.value = await response.json()
            form.value = {
                name: profile.value.name || '',
                hr_contact: profile.value.hr_contact || '',
                website: profile.value.website || ''
            }
        } catch (err) {
            message.value = 'Error loading profile.'
            console.error(err)
        }
    }

    async function saveProfile() {
        loading.value = true
        message.value = ''
        try {
            const response = await fetch(`${API_BASE_URL}/api/company-profile`, {
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
            await fetchProfile()  // Refresh to show pending changes
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
        form.value = {
            name: profile.value.name || '',
            hr_contact: profile.value.hr_contact || '',
            website: profile.value.website || ''
        }
        message.value = ''
    }
</script>

<template>
    <div class="profile-container">
        <h2>Company Profile</h2>
        
        <div v-if="!editing">
            <div class="profile-info">
                <p><strong>Name:</strong> {{ profile.name }}</p>
                <p><strong>Email:</strong> {{ profile.email }}</p>
                <p><strong>HR Contact:</strong> {{ profile.hr_contact }}</p>
                <p><strong>Website:</strong> {{ profile.website }}</p>
                <p><strong>Approval Status:</strong> {{ profile.approval_status }}</p>
                
                <div v-if="profile.pending_name || profile.pending_hr_contact || profile.pending_website" class="pending-changes">
                    <h3>Pending Changes (Awaiting Admin Approval)</h3>
                    <p v-if="profile.pending_name"><strong>Name:</strong> {{ profile.pending_name }}</p>
                    <p v-if="profile.pending_hr_contact"><strong>HR Contact:</strong> {{ profile.pending_hr_contact }}</p>
                    <p v-if="profile.pending_website"><strong>Website:</strong> {{ profile.pending_website }}</p>
                </div>
            </div>
            <button @click="startEditing" class="edit-btn">Edit Profile</button>
        </div>
        
        <div v-else>
            <form @submit.prevent="saveProfile" class="edit-form">
                <label>Name</label>
                <input v-model="form.name" type="text" required />
                
                <label>HR Contact</label>
                <input v-model="form.hr_contact" type="tel" pattern="[0-9]{10}" placeholder="+91" required />
                
                <label>Website</label>
                <input v-model="form.website" type="text" placeholder="example.com" />
                
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
    
    .pending-changes {
        margin-top: 20px;
        padding: 15px;
        border: 1px solid orange;
        border-radius: 8px;
        background-color: #FFF8E1;
    }
    
    .pending-changes h3 {
        margin-top: 0;
        color: orange;
        font-family: "Bebas Neue", sans-serif;
    }
    
    .edit-form {
        display: flex;
        flex-direction: column;
    }
    
    label {
        margin-top: 15px;
        font-family: "Montserrat", sans-serif;
    }
    
    input {
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
    }
    
    .message:contains("submitted") {
        background-color: #E8F5E8;
        color: green;
    }
</style>
