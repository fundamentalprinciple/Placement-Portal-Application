<script setup>
    import Hello from '@/components/Hello.vue'
    import CreateDrive from '@/features/company/CreateDrive.vue'
    import ViewDrives from '@/features/company/ViewDrives.vue'
    //import ManageApplications from '@/features/company/ManageApplications.vue'
    //import ScheduleInterview from '@/features/company/ScheduleInterview.vue'
    //import Recruit from '@/features/company/Recruit.vue'

</script>

<template>
    <Hello />
    <div class="controls">
        <CreateDrive />
        <ViewDrives />
    </div>
</template>

<style scoped>
    .controls {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }
</style>
