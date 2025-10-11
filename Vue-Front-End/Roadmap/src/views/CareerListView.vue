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
      <!-- Title -->
      <h3
        class="text-2xl font-spacegrotesk font-bold mb-2"
        :style="{ color: 'var(--accent-cyan)' }"
      >
        {{ career.name }}
      </h3>

      <!-- Meta Info -->
      <p class="opacity-80 text-sm mb-3">
        {{ getSectorName(career.sector_id) }} • {{ career.duration_years }} years education
      </p>

      <!-- Overview -->
      <p class="opacity-70 text-sm mb-4">{{ career.overview }}</p>

      <!-- Salary -->
      <p class="text-sm mb-4">
        <strong :style="{ color: 'var(--accent-green)' }">
          R{{ Number(career.average_salary || 0).toLocaleString() }}
        </strong>
        /year (average)
      </p>

      <!-- Outlook -->
      <p class="text-xs opacity-70 italic mb-4">
        {{ career.job_outlook }}
      </p>
    </div>

    <!-- View Details Button -->
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
import { useApiData } from '@/hooks/useApiData'

const { data, fetchData } = useApiData()
const careers = ref([])
const sectors = ref([])

const fetchCareers = async () => {
  await fetchData('/careers')
  careers.value = data.value || []
}

const fetchSectors = async () => {
  await fetchData('/sectors')
  sectors.value = data.value || []
}

const getSectorName = (id) => {
  const sector = sectors.value.find(s => s.id === id)
  return sector ? sector.name : 'Unknown Sector'
}

onMounted(async () => {
  await fetchSectors()
  await fetchCareers()
})

</script>


<style scoped>
/* Subtle card hover transitions */
a:hover {
  filter: brightness(1.1);
  transition: all 0.3s ease;
}
</style>
