<!--views/CareerListView.vue-->
<template>
  <div
    class="flex flex-col flex-grow p-8 transition-all duration-300"
    :style="{ backgroundColor: 'var(--card-color)', color: 'var(--text-color)' }"
  >
    <!-- Header -->
    <header class="text-center mb-10 border-b pb-6 max-w-5xl mx-auto">
      <h1
        class="text-4xl md:text-5xl font-spacegrotesk font-bold mb-3"
        :style="{ color: 'var(--accent-cyan)' }"
      >
        Explore All Career Profiles
      </h1>
      <p class="text-lg opacity-80 max-w-3xl mx-auto">
        Browse through detailed profiles and choose a pathway that matches your skills and goals.
      </p>
    </header>

    <!-- Career Cards Grid -->
    <section class="max-w-6xl mx-auto w-full grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
  <div
    v-for="career in careers"
    :key="career.id"
    class="p-6 rounded-xl border shadow-md transition-all duration-200 hover:scale-[1.02] hover:shadow-lg flex flex-col justify-between"
    :style="{
      backgroundColor: 'var(--card-color)',
      borderColor: 'var(--accent-blue)',
    }"
  >
    <div>
      <span
        class="text-xs font-semibold px-2 py-0.5 rounded-full"
        :style="{ backgroundColor: 'var(--accent-green)', color: 'var(--bg-color)' }"
      >
        {{ career.sector?.name || 'Uncategorized' }}
      </span>
      <h3
        class="text-2xl font-spacegrotesk font-bold mt-2 mb-2"
        :style="{ color: 'var(--accent-cyan)' }"
      >
        {{ career.name }}
      </h3>
      <p class="text-sm opacity-70 mb-4 line-clamp-3">{{ career.overview }}</p>

      <!-- Salary / Outlook -->
      <div class="flex flex-col space-y-1 text-sm mt-4">
        <div class="flex items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="2"
            stroke="currentColor"
            class="w-4 h-4 mr-2"
            :style="{ color: 'var(--accent-green)' }"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
          <span class="font-medium">Avg. Salary:</span> R{{ career.average_salary.toLocaleString() }}
        </div>
        <div class="flex items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="2"
            stroke="currentColor"
            class="w-4 h-4 mr-2"
            :style="{ color: 'var(--accent-blue)' }"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m-6 0h6"
            />
          </svg>
          <span class="font-medium">Job Outlook:</span> {{ career.job_outlook || 'N/A' }}
        </div>
      </div>
    </div>
    
    <!-- Link to Detail View -->
    <router-link
      :to="`/careers/${career.id}`"
      class="mt-4 inline-flex items-center justify-center px-4 py-2 rounded-lg font-semibold transition-all duration-200"
      :style="{
        backgroundColor: 'var(--accent-blue)',
        color: 'var(--bg-color)',
        boxShadow: '0 0 8px var(--accent-blue)',
      }"
    >
      View Details
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="2"
        stroke="currentColor"
        class="w-4 h-4 ml-2"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
      </svg>
    </router-link>
  </div>
</section>


  
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCareers } from '@/api/careerService'

const careers = ref([])
const loading = ref(true)
const error = ref(null)

const fetchCareers = async () => {
  try {
    loading.value = true
    const response = await getCareers()
    careers.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || err.message
    console.error('Error fetching careers:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchCareers)
</script>


<style scoped>
/* Scoped styles */
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
