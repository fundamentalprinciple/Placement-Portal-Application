<script setup>
    import Hello from '@/components/Hello.vue'
    import ManageStudentProfiles from '@/features/admin/ManageStudentProfiles.vue'

</script>

<template>
    <Hello />
    <div class="controls">
        
        <ManageStudentProfiles />
        <!--
        <ManageCompanyProfiles />
        <ManageDrives />
        <ViewPlacementStatistics />
        -->
    </div>

</template>

<style scoped>
    .controls {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }
</style>
