<script setup>
    import { useRoute } from 'vue-router'
    import About from '@/components/About.vue'

    const route = useRoute()
</script>

<template>
  <div>
    <About v-if="route.path === '/' || route.path === '/about'" />
  </div>
</template>

<style scoped>
</style>
