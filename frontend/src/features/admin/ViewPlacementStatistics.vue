<script setup>
    import { ref, onMounted } from 'vue'
    import { useAuthStore } from '@/stores/auth'

    const auth = useAuthStore()

    const stats = ref({
        total_placements: 0,
        placements_by_department: [],
        placements_by_date: [],
        top_companies: [],
        pending_recruitment_requests: 0,
        recruited_students: 0,
        total_students: 0,
        placement_rate: '0%'
    })

    async function fetchStatistics() {
        const response = await fetch("http://localhost:3000/api/get-placement-statistics", {
            method: "GET",
            headers: {
                "Authentication-Token": auth.token
            }
        })
        
        if (response.ok) {
            stats.value = await response.json()
        }
    }

    onMounted(async () => {
        await fetchStatistics()
        console.log(stats.placements_by_department)
    })
</script>


<template>
    <div class="container">
        <h2>Placement Statistics</h2>
        
        <div class="stats-grid">
            <div class="stat-card">
                <p class="stat-label">Total Placements</p>
                <p class="stat-value">{{ stats.total_placements }}</p>
            </div>
            
            <div class="stat-card">
                <p class="stat-label">Placement Rate</p>
                <p class="stat-value">{{ stats.placement_rate }}</p>
            </div>
            
            <div class="stat-card">
                <p class="stat-label">Recruited Students</p>
                <p class="stat-value">{{ stats.recruited_students }}/{{ stats.total_students }}</p>
            </div>
            
            <div class="stat-card">
                <p class="stat-label">Pending Recruitments</p>
                <p class="stat-value">{{ stats.pending_recruitment_requests }}</p>
            </div>
        </div>

        <div class="charts-section">
            <div class="chart-container">
                <h3>Placements by Department</h3>
                <div v-for="dept in stats.placements_by_department" :key="dept.department" class="chart-item">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>{{ dept.department }}</span>
                        <span style="font-weight: bold;">{{ dept.count }}</span>
                    </div>
                    <div style="background-color: #e0e0e0; border-radius: 5px; height: 20px; overflow: hidden;">
                        <div 
                            :style="{
                                width: `${(dept.count / Math.max(...stats.placements_by_department.map(d => d.count), 1)) * 100}%`,
                                backgroundColor: '#4CAF50',
                                height: '100%'
                            }"
                        ></div>
                    </div>
                </div>
            </div>

            <div class="chart-container">
                <h3>Top Companies</h3>
                <div v-if="stats.top_companies.length > 0">
                    <div v-for="company in stats.top_companies" :key="company.company" class="chart-item">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span>{{ company.company }}</span>
                            <span style="font-weight: bold;">{{ company.count }}</span>
                        </div>
                        <div style="background-color: #e0e0e0; border-radius: 5px; height: 20px; overflow: hidden;">
                            <div 
                                :style="{
                                    width: `${(company.count / Math.max(...stats.top_companies.map(c => c.count), 1)) * 100}%`,
                                    backgroundColor: '#2196F3',
                                    height: '100%'
                                }"
                            ></div>
                        </div>
                    </div>
                </div>
                <p v-else style="text-align: center; color: #999;">No placement data yet</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    h1, h2, h3 {
        font-family: "Bebas Neue", sans-serif;
        text-align: center;
    }

    p, span, div {
        font-family: "Montserrat", sans-serif;
    }

    .container {
        border: 1px solid lightblue;
        border-radius: 10px;
        background-color: #ECEBFA;
        width: 100%;
        max-width: 1000px;
        padding: 40px;
        box-shadow: 10px 10px 5px lightblue;
        margin: 20px auto;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 40px;
    }

    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .stat-label {
        font-size: 14px;
        opacity: 0.9;
        margin: 0;
    }

    .stat-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0 0 0;
    }

    .charts-section {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
    }

    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .chart-container h3 {
        margin-top: 0;
        color: #333;
    }

    .chart-item {
        margin-bottom: 20px;
    }
</style>
