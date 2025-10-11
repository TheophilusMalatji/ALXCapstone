<template>
  <article class="bg-white border rounded-lg p-4 shadow-sm hover:shadow-md transition">
    <header class="mb-3">
      <h3 class="text-lg font-medium">{{ roadmap.title }}</h3>
      <p class="text-sm text-gray-600">{{ roadmap.description }}</p>
    </header>

    <ul class="text-sm text-gray-700 space-y-1 mb-4">
      <li v-for="lvl in roadmap.levels" :key="lvl.id" class="flex items-center justify-between">
        <span>{{ lvl.title }}</span>
        <span class="text-xs px-2 py-0.5 rounded-full border">{{ lvl.status }}</span>
      </li>
    </ul>

    <div class="flex justify-between items-center">
      <router-link :to="`/roadmaps/${roadmap.id}`" class="text-sm text-blue-600 hover:underline">Open</router-link>
      <div class="text-xs text-gray-500">ID: {{ roadmap.id }}</div>
    </div>
  </article>
</template>

<script setup>
defineProps({
  roadmap: {
    type: Object,
    required: true
  }
})
</script>
