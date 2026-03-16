<script setup>
    import { ref, inject } from 'vue'

    const name = inject("name")
    const role = inject("role")

    const Name = name._value.charAt(0).toUpperCase() + name._value.slice(1)

</script>

<template>
    <div class="greet">
        <h1>{{role}} Dashboard</h1>
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
