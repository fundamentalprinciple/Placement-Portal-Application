<script setup>
    import { ref, onMounted } from 'vue'
    import { useDriveStore } from '@/stores/drives'

    const driveStore = useDriveStore()
    const loading = ref(true)
    const error = ref('')

    onMounted(async () => {
        try {
            await driveStore.fetchCompanyInterviews()
        } catch (err) {
            error.value = 'Unable to load interviews.'
        } finally {
            loading.value = false
        }
    })

    async function cancelInterview(interview_id) {
        await driveStore.cancelCompanyInterview(interview_id)
        await driveStore.fetchCompanyInterviews()
    }

    async function completeInterview(interview_id) {
        await driveStore.completeCompanyInterview(interview_id)
        await driveStore.fetchCompanyInterviews()
    }
</script>

<template>
    <div class="container">
        <h2>Scheduled Interviews</h2>
        <div v-if="loading" class="message">Loading interviews...</div>
        <div v-else-if="error" class="message error">{{ error }}</div>
        <div v-else-if="driveStore.interviews.length === 0" class="message">
            No interviews scheduled.
        </div>
        <div v-else>
            <div v-for="interview in driveStore.interviews" :key="interview.id" class="profile">
                <h4>{{ interview.student_name }}</h4>
                <p><strong>Message:</strong> {{ interview.company_message }}</p>
                <p><strong>Date:</strong> {{ interview.interview_date }}</p>
                <p><strong>Time:</strong> {{ interview.interview_time }}</p>
                <p><strong>Address:</strong> {{ interview.interview_address }}</p>
                <p><strong>Accepted:</strong> {{ interview.accepted ? 'Yes' : 'No' }}</p>
                <p><strong>Completed:</strong> {{ interview.completed ? 'Yes' : 'No' }}</p>
                <button @click="completeInterview(interview.id)" :disabled="interview.completed">
                    Mark Completed
                </button>
                <button @click="cancelInterview(interview.id)">
                    Cancel
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .container {
        border: 1px solid lightblue;
        border-radius: 10px;
        background-color: #ECEBFA;
        width: 400px;
        padding: 30px;
        box-shadow: 10px 10px 5px lightblue;
    }
    .profile {
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid lightblue;
        border-radius: 10px;
        box-shadow: 5px 5px 5px lightblue;
    }
    .message {
        font-family: "Montserrat", sans-serif;
        text-align: center;
        margin-bottom: 20px;
    }
    button {
        background-color: lightblue;
        border: none;
        border-radius: 10px;
        padding: 10px;
        margin-right: 10px;
        cursor: pointer;
    }
    button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    .error {
        color: red;
    }
</style>
