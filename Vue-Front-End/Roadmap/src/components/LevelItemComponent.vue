<template>
  <div class="bg-white border rounded p-3 shadow-sm flex items-start gap-4">
    <div class="flex-shrink-0">
      <div class="w-9 h-9 rounded-full border flex items-center justify-center text-sm font-medium">
        {{ level.id }}
      </div>
    </div>
    <div class="flex-1">
      <div class="flex justify-between items-start">
        <h4 class="font-medium">{{ level.title }}</h4>
        <span class="text-xs text-gray-600">{{ level.status }}</span>
      </div>
      <p class="text-sm text-gray-600 mt-1">This is a placeholder description for the level.</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  level: {
    type: Object,
    required: true
  }
})
</script>
