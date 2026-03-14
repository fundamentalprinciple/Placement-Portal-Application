<script setup>
    import { ref } from "vue"
    import { useRoute } from 'vue-router'    
    
    const route = useRoute()
    
    const username = ref("")
    const password = ref("")



</script>

<template>
    <form>
        <fieldset>
            <legend>Login</legend>
            <label for="username">Username</label>
            <input v-model="username" id="username" name="username" type="text" required />
            <br />
            <label for="password">Password</label>
            <input v-model="password" id="password" name="password" type="password" required />
            <br />
            <button type="submit">Submit</button>
            <br />
            <p>If you don't have an account, register as a <RouterLink to="/register-student">Student</RouterLink> or <RouterLink to="/register-companyh">Company</RouterLink></p>
        </fieldset>
    </form>
</template>

<style scoped>
</style>
