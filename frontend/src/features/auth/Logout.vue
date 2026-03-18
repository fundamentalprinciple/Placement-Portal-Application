<script setup>
    import { onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { useAuthStore } from '@/stores/auth'

    const router = useRouter();
    const auth = useAuthStore()

    onMounted(() => {
        auth.logout()
        router.push('/login')
    })

</script>

<template>
</template>

<style scoped>
</style>
