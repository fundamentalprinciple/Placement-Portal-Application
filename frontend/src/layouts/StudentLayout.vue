<script setup>
    import Hello from '@/components/Hello.vue'
    import ApplyDrive from '@/features/student/ApplyDrive.vue'
    import AppliedDrives from '@/features/student/AppliedDrives.vue'    

</script>

<template>
    <Hello />
    <div class="controls">
        <ApplyDrive />
        <AppliedDrives />
    </div>
</template>

<style scoped>
     .controls {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }
    
       
</style>
