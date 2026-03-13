<script setup></script>

<template>
    <nav class="navbar navbar-expand-lg">
        <img class="navbar-brand" src="/Logo.svg" height="50" width="50" />
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <RouterLink to="/">Home</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink to="/login">Login</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink to="/about">About</RouterLink>
                </li>
            </ul>
        </div>
    </nav>
</template>

<style scoped>
    nav {
        border: 1px solid black;
    }
</style>
