<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const auth = useAuthStore()

onMounted(() => {
  auth.authenticate()
})

watch(() => route.path, () => {
  auth.authenticate()
})

watch([
  () => auth.token,
  () => auth.username
], () => {
  auth.authenticate()
})

</script>

<template>
    <Navbar />
    <main>
        <RouterView /> 
    </main>
</template>

<style scoped>
</style>
