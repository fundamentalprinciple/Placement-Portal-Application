<script setup>
    import { ref, inject } from 'vue'

    const token = localStorage.getItem('Authentication-Token')
    
    let studentList = ref([]);

    async function getStudentProfiles() {
        const response = await fetch("http://localhost:3000/api/manage-student-profiles", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": token 
            },
        })
        
        studentList.value = await response.json()
    }    

    getStudentProfiles()

    async function changeAccountStatus(id,new_status) {
        const response = await fetch("http://localhost:3000/api/manage-student-profiles", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": token
            },
            body: JSON.stringify({
                id: id,
                new_status: new_status
            })
        })
        await getStudentProfiles();
    }

    

</script>

<template>
   <div class="container">
        <h2>Student Profiles</h2>
        <div v-for="student in studentList" class="profile">
            <h4>{{ student.name }}</h4>
            <p><strong>Major:</strong>           {{ student.degree }}</p>
            <p><strong>CGPA:</strong>            {{ student.cgpa }}</p>
            <p><strong>Year:</strong>            {{ student.year }}</p>
            <p v-if="student.available==true"><strong>Available:</strong>       Yes</p>
            <p v-if="student.available==false"><strong>Available:</strong>       No</p>

            <button @click="changeAccountStatus(student.id,'deactivate')" v-if="student.account_status==true" >Deactivate Account</button>
            <button @click="changeAccountStatus(student.id,'activate')" v-if="student.account_status==false">Activate Account</button>
            

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
        width: 400px;
        padding-top: 50px;
        padding-bottom: 50px;
        box-shadow: 10px 10px 5px lightblue;
        margin-bottom: 50px;
    }

    .profile {
        padding: 20px;
        margin: auto;
        margin-bottom: 20px;
        border: 1px solid lightblue;
        border-radius: 10px;
        width: 300px;           
        box-shadow: 5px 5px 5px lightblue;
    }

    button {
        background-color: lightblue;
        border: none;
        border-radius: 10px;
        padding: 10px;
        margin-left: 40px;
    }   

    button:hover {
        background-color: #E3D888;    
    }    

</style>
