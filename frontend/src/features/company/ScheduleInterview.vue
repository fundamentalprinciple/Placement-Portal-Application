<script setup>
    import { ref } from 'vue'
    import { useAuthStore } from '@/stores/auth'
    import { useDriveStore } from '@/stores/drives'

    const props = defineProps({
        application: { type: Object, required: true }
    })

    const auth = useAuthStore()
    const driveStore = useDriveStore();
    const open = ref(false)
    const message = ref('')
    const address = ref('')
    const date = ref('')
    const time = ref('')
    const submitting = ref(false)
    const success = ref('')
    const error = ref('')

    function toggleForm() {
        open.value = !open.value
        success.value = ''
        error.value = ''
    }

    async function submitInterview() {
        success.value = ''
        error.value = ''

        if (!message.value || !address.value || !date.value || !time.value) {
            error.value = 'All fields are required.'
            return
        }

        submitting.value = true
        try {
            const response = await fetch('http://localhost:3000/api/schedule-interview', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': auth.token
                },
                body: JSON.stringify({
                    student_id: props.application.student_id,
                    message: message.value,
                    address: address.value,
                    date: date.value,
                    time: time.value
                })
            })

            const data = await response.json()

            if (!response.ok) {
                error.value = data.message || 'Unable to schedule interview.'
                return
            }

            success.value = data.message || 'Interview scheduled successfully.'
            open.value = false
            message.value = ''
            address.value = ''
            date.value = ''
            time.value = ''
            await driveStore.fetchCompanyInterviews()
        } catch (err) {
            error.value = 'Network error while scheduling interview.'
            console.error(err)
        } finally {
            submitting.value = false
        }
    }
</script>

<template>
    <div class="schedule-block">
        <button class="toggle-btn" @click="toggleForm">
            {{ open ? 'Cancel Interview' : 'Schedule Interview' }}
        </button>

        <div v-if="open" class="form-panel">
            <label>Message</label>
            <textarea v-model="message" rows="3" />

            <label>Address</label>
            <input v-model="address" type="text" />

            <label>Date</label>
            <input v-model="date" type="date" />

            <label>Time</label>
            <input v-model="time" type="time" />

            <button class="submit-btn" @click="submitInterview" :disabled="submitting">
                {{ submitting ? 'Scheduling...' : 'Send Interview Invite' }}
            </button>

            <div v-if="success" class="success">{{ success }}</div>
            <div v-if="error" class="error">{{ error }}</div>
        </div>
    </div>
</template>

<style scoped>
    .schedule-block {
        margin-top: 16px;
    }

    .toggle-btn,
    .submit-btn {
        background-color: lightblue;
        border: none;
        border-radius: 8px;
        padding: 10px 14px;
        font-family: "Montserrat", sans-serif;
        cursor: pointer;
    }

    .form-panel {
        margin-top: 12px;
        padding: 14px;
        border: 1px solid lightblue;
        border-radius: 10px;
        background: #fff;
    }

    label {
        display: block;
        margin-top: 10px;
        font-family: "Montserrat", sans-serif;
    }

    input,
    textarea {
        width: 100%;
        border: 1px solid lightblue;
        border-radius: 8px;
        padding: 10px;
        margin-top: 6px;
        font-family: "Montserrat", sans-serif;
    }

    .success {
        margin-top: 10px;
        color: green;
        font-family: "Montserrat", sans-serif;
    }

    .error {
        margin-top: 10px;
        color: red;
        font-family: "Montserrat", sans-serif;
    }
</style>
