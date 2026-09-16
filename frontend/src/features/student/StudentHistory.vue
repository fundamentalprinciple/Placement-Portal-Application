<script setup>
import { API_BASE_URL } from '@/config/api'
    import { ref, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { useAuthStore } from '@/stores/auth'

    const auth = useAuthStore()
    const router = useRouter()

    const history = ref([])

    async function fetchHistory() {
        const response = await fetch(`${API_BASE_URL}/api/get-placement-history`, {
            method: "GET",
            headers: {
                "Authentication-Token": auth.token
            }
        })
        if (response.ok) {
            history.value = await response.json()
        }
    }

    function exportHistory() {
        const csvContent = "data:text/csv;charset=utf-8,"
            + "Type,Status,Date,Company,Position,Description\n"
            + history.value.map(item => 
                `${item.type},${item.status},${item.date},${item.company_name},${item.job_title},"${item.description}"`
            ).join("\n")
        
        const encodedUri = encodeURI(csvContent)
        const link = document.createElement("a")
        link.setAttribute("href", encodedUri)
        link.setAttribute("download", "placement_history.csv")
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }

    function goBack() {
        router.push('/')
    }

    onMounted(async () => {
        await fetchHistory()
    })
</script>

<template>
    <div style="margin-top: 50px;" class="container">
        <h2>Placement History</h2>
        
        <div class="actions">
            <button @click="exportHistory">Export History</button>
            <button @click="goBack">Go Back to Dashboard</button>
        </div>
        
        <div v-for="item in history" :key="item.date + item.type" class="history-card">
            <h4>{{ item.description }}</h4>
            <p><strong>Status:</strong> {{ item.status }}</p>
            <p><strong>Date:</strong> {{ item.date }}</p>
            <p><strong>Company:</strong> {{ item.company_name }}</p>
            <p><strong>Position:</strong> {{ item.job_title }}</p>
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
        width: 550px;
        padding-top: 50px;
        padding-bottom: 50px;
        box-shadow: 10px 10px 5px lightblue;
        margin-bottom: 50px;
    }

    .actions {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
        padding: 0 20px;
    }

    .history-card {
        padding: 20px;
        margin: auto;
        margin-bottom: 20px;
        border: 1px solid lightblue;
        border-radius: 10px;
        width: 400px;
        box-shadow: 5px 5px 5px lightblue;
    }

    button {
        background-color: lightblue;
        border: none;
        border-radius: 10px;
        padding: 10px;
        cursor: pointer;
    }

    button:hover {
        background-color: #E3D888;
    }
</style>
