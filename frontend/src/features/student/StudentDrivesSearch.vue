<script setup>
import { API_BASE_URL } from '@/config/api'
    import { ref } from 'vue'
    import { useAuthStore } from '@/stores/auth'

    const auth = useAuthStore()
    const query = ref('')
    const results = ref([])
    const showResults = ref(false)

    async function searchDrives() {
        const term = query.value.trim()
        if (!term) {
            results.value = []
            showResults.value = false
            return
        }

        const response = await fetch(`${API_BASE_URL}/api/search-drives`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': auth.token
            },
            body: JSON.stringify({ search: term })
        })

        const data = await response.json()
        results.value = Array.isArray(data) ? data : []
        showResults.value = true
    }

    function handleResultClick(item) {
        query.value = ''
        results.value = []
        showResults.value = false
        // Optionally scroll to or highlight the drive in the list
        window.scrollTo(0, document.body.scrollHeight)
    }

    function handleInputChange() {
        if (!query.value.trim()) {
            results.value = []
            showResults.value = false
        }
    }

    function handleSubmit(e) {
        e.preventDefault()
        searchDrives()
    }
</script>

<template>
    <div class="search-container">
        <form @submit="handleSubmit">
            <input 
                v-model="query" 
                @input="handleInputChange"
                type="text" 
                placeholder="Search by company name..."
                class="search-input"
            />
            <button type="submit" class="search-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                </svg>
            </button>
        </form>
        <div v-if="showResults && results.length > 0" class="results-dropdown">
            <div 
                v-for="item in results" 
                :key="`${item.id}`"
                class="result-item"
                @click="handleResultClick(item)"
            >
                {{ item.label }}
            </div>
        </div>
        <div v-else-if="showResults && query.trim() && results.length === 0" class="no-results">
            No drives found
        </div>
    </div>
</template>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    .search-container {
        background-color: #ECEBFA;
        border: 1px solid lightblue;
        border-radius: 10px;
        padding: 15px;
        margin: 0 10px;
        width: 300px;
        box-shadow: 10px 10px 5px rgba(173, 188, 255, 0.35);
        position: relative;
        display: inline-block;
    }

    form {
        display: flex;
        gap: 8px;
    }

    .search-input {
        flex: 1;
        padding: 10px 12px;
        border: 1px solid lightblue;
        border-radius: 8px;
        font-family: "Montserrat", sans-serif;
        font-size: 13px;
        outline: none;
    }

    .search-input:focus {
        border-color: #7B9FD3;
        box-shadow: 0 0 5px rgba(173, 188, 255, 0.5);
    }

    .search-btn {
        background-color: lightblue;
        border: none;
        border-radius: 8px;
        padding: 10px 12px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background-color 0.2s;
    }

    .search-btn:hover {
        background-color: #9FBFF0;
    }

    .results-dropdown {
        position: absolute;
        top: calc(100% + 5px);
        left: 0;
        right: 0;
        background: white;
        border: 1px solid lightblue;
        border-radius: 8px;
        max-height: 200px;
        overflow-y: auto;
        z-index: 10;
        box-shadow: 0 4px 8px rgba(173, 188, 255, 0.35);
    }

    .result-item {
        padding: 10px 12px;
        font-family: "Montserrat", sans-serif;
        font-size: 13px;
        cursor: pointer;
        border-bottom: 1px solid #f0f0f0;
        transition: background-color 0.2s;
    }

    .result-item:last-child {
        border-bottom: none;
    }

    .result-item:hover {
        background-color: #ECEBFA;
    }

    .no-results {
        position: absolute;
        top: calc(100% + 5px);
        left: 0;
        right: 0;
        background: white;
        border: 1px solid lightblue;
        border-radius: 8px;
        padding: 10px 12px;
        font-family: "Montserrat", sans-serif;
        font-size: 13px;
        color: #999;
        z-index: 10;
    }
</style>
