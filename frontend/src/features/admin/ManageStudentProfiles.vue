<script setup>
    import { inject } from 'vue'

    const token = localStorage.getItem('Authentication-Token')
    

    async function getStudentProfiles() {
        const response = await fetch("http://localhost:3000/api/manage-student-profiles", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": token 
            },
        })
        
        const dataList = await response.json()
        console.log("Here goes: ")
        for (const list of dataList) {
            console.log(list)
        }
    }    

    getStudentProfiles()

</script>

<template>
    
</template>
