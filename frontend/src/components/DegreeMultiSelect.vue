<template>
  <div style="width:300px; position:relative; font-family:sans-serif;">
    <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:6px;">
      <div
        v-for="item in modelValue"
        :key="item"
        style="background:#e0e7ff; padding:5px 10px; border-radius:20px; display:flex; align-items:center;"
      >
        {{ item }}
        <span
          @click.stop="removeDegree(item)"
          style="margin-left:8px; cursor:pointer; font-weight:bold;"
        >×</span>
      </div>
    </div>

    <div
      @click="toggleDropdown"
      style="border:1px solid #ccc; padding:8px; border-radius:8px; cursor:pointer; background-color: white;"
    >
      <span v-if="modelValue.length">
        {{ modelValue.join(', ') }}
      </span>
      <span v-else>
        Select Degree
      </span>
    </div>

    <div
      v-if="isOpen"
      style="position:absolute; top:100%; left:0; width:100%; border:1px solid #ccc; border-radius:8px; background:white; max-height:150px; overflow-y:auto; z-index:10;"
    >
      <div
        v-for="option in degrees"
        :key="option"
        @click.stop="selectDegree(option)"
        style="padding:8px; cursor:pointer;"
      >
        {{ option }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)

const degrees = [
  "Computer Engineering",
  "Computer Science Engineering",
  "Electrical Engineering",
  "Mechanical Engineering",
  "Civil Engineering",
  "Chemical Engineering",
  "Aerospace Engineering",
  "Automotive Engineering",
  "Robotics Engineering",
  "Nanotechnology Engineering",
  "Data Science and Applications",
  "Electronic Systems",
  "Management and Data Science"
]

function toggleDropdown() {
  isOpen.value = !isOpen.value
}

function selectDegree(option) {
  if (!props.modelValue.includes(option)) {
    emit('update:modelValue', [...props.modelValue, option])
  }
}

function removeDegree(option) {
  emit('update:modelValue', props.modelValue.filter(item => item !== option))
}
</script>

<style scoped>
div[style*="cursor:pointer"]:hover {
  background: #f3f4f6;
}
</style>
