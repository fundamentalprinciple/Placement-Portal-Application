<script setup>
    import { ref } from 'vue'
    import { useAuthStore } from '@/stores/auth'

    const auth = useAuthStore()

    const Name = auth.name.charAt(0).toUpperCase() + auth.name.slice(1)

</script>

<template>
    <div class="greet">
        <h1>{{auth.role}} Dashboard</h1>
        <p>Welcome, {{Name}}</p>
    </div>
</template>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');
    
    h1{
        font-family: "Bebas Neue", sans-serif;
    }

    p {
        font-family: "Montserrat", sans-serif;
    }
    
    .greet {
        padding: 30px;
        text-align: center;
    }
   
</style>
