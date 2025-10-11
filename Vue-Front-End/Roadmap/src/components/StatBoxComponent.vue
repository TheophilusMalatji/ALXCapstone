<template>
  <div class="inline-block bg-gray-100 rounded p-2 text-center min-w-[80px]">
    <div class="text-sm text-gray-600">{{ label }}</div>
    <div class="text-lg font-semibold">{{ value }}</div>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, default: '' },
  value: { type: [String, Number], default: 0 }
})
</script>
