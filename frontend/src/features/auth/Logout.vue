<script setup>
    import { onMounted } from 'vue'
    import { useRouter } from 'vue-router'

    const router = useRouter();

    onMounted(() => {
        localStorage.removeItem('Authentication-Token');
        localStorage.removeItem('username');

        router.push('/login')
    })

</script>

<template>
</template>

<style scoped>
</style>
