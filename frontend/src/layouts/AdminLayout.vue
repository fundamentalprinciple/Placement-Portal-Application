<script setup>
    import Hello from '@/components/Hello.vue'
    import ManageStudentProfiles from '@/features/admin/ManageStudentProfiles.vue'
    import ManageCompanyProfiles from '@/features/admin/ManageCompanyProfiles.vue'
    import ManageDrives from '@/features/admin/ManageDrives.vue'

</script>

<template>
    <Hello />
    <div class="controls">
        
        <ManageStudentProfiles />
        <ManageCompanyProfiles />
        <ManageDrives />
        <!--
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
