<script setup>
    import { useAuthStore } from '@/stores/auth'

    const auth = useAuthStore()

</script>

<template>
    <nav class="navbar navbar-expand-lg">
        <div class="logo">
            <img class="navbar-brand" src="/Logo.svg" height="100" width="100" />
            <p>Placement Portal</p>
        </div>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span style="height: 20px; width: 20px; margin-bottom: 10px;" class="navbar-toggler-icon"></span>
    </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li v-if="auth.isAuthenticated" class="nav-item">
                    <RouterLink class="link" to="/">Home</RouterLink>
                </li>
                
                <li class="nav-item">
                    <RouterLink v-if="auth.isAuthenticated" class="link" to="/logout">Logout</RouterLink>
                    <RouterLink v-else class="link" to="/login">Login</RouterLink>
                </li>

                <li class="nav-item">
                    <RouterLink class="link" to="/about">About</RouterLink>
                </li>
            </ul>
        </div>
    </nav>
</template>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    nav {
        background-color: #773344;
    }
    .logo {
        margin-left: 10%;
        padding: 5px;
        color: white;
        display: flex;
        flex-direction: row;
    }
    .navbar-brand {
        margin-left: -20px;
    }
    p {
        font-family: "Bebas Neue", sans-serif;
        font-size: xx-large; 
        margin: auto;
        margin-left: -16px;
    }

    .navbar-toggler {
        background-color: white;
        margin-right: 10%;
        height: 30px;
    }

    .navbar-toggler:hover {
        background-color: #E3D888;
    }

    .link {
        font-family: "Montserrat", sans-serif;
        text-decoration: none;
        color: white;
        margin-right: 5vw;
    }
    
    .nav-item {
        margin-top: 10px;
    }
    
    .link:hover {
        color: #E3D888; 
    }

    .navbar-nav {
        margin-left: 45%; 
    }
</style>
