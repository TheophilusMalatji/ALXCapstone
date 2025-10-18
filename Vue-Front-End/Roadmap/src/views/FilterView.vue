<!--views/FilterView.vue-->
<template>
  <div class="flex flex-col flex-grow p-8 space-y-10 transition-all duration-300"
       :style="{ backgroundColor: 'var(--card-color)', color: 'var(--text-color)' }">
    
    <!-- Header -->
    <header class="text-center border-b pb-6 max-w-5xl mx-auto">
      <h1 class="text-4xl md:text-5xl font-spacegrotesk font-bold mb-3"
          :style="{ color: 'var(--accent-cyan)' }">
        Career Pathway Filter
      </h1>
      <p class="text-lg opacity-80 max-w-3xl mx-auto">
        Narrow down career paths based on your education time, salary expectations, and preferred sectors.
      </p>
    </header>

    <!-- Filter Section -->
    <section class="max-w-5xl mx-auto w-full">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-6 rounded-xl border shadow-md"
           :style="{ backgroundColor: 'var(--bg-color)', borderColor: 'var(--accent-blue)' }">

        <!-- Education Duration -->
        <div class="flex flex-col space-y-2">
          <label class="text-sm font-semibold">Maximum Study Duration (Years: {{ duration }})</label>
          <input type="range" min="1" max="8" v-model.number="duration" class="w-full accent-[var(--accent-cyan)]" @change="applyFilters">
          <p class="text-xs opacity-70">Find careers with an education roadmap up to {{ duration }} years.</p>
        </div>

        <!-- Minimum Salary -->
        <div class="flex flex-col space-y-2">
          <label class="text-sm font-semibold">Minimum Average Salary (R)</label>
          <input type="number" placeholder="Enter minimum salary..." v-model="salary" class="p-2 rounded-lg border focus:ring-2"
                 :style="{ borderColor: 'var(--accent-green)', backgroundColor: 'var(--card-color)', color: 'var(--text-color)', focusRing: 'var(--accent-green)' }"
                 @input="applyFilters">
          <p class="text-xs opacity-70">Filter careers by minimum average salary.</p>
        </div>

        <!-- Sector Filter -->
        <div class="flex flex-col space-y-2">
          <label class="text-sm font-semibold">Filter by Sector</label>
          <select v-model="sector" class="p-2 rounded-lg border focus:ring-2"
                  :style="{ borderColor: 'var(--accent-blue)', backgroundColor: 'var(--card-color)', color: 'var(--text-color)', focusRing: 'var(--accent-blue)' }"
                  @change="applyFilters">
            <option value="">All Sectors</option>
            <option v-for="s in sectors" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
          <p class="text-xs opacity-70">Select a specific sector to focus your search.</p>
        </div>
      </div>
    </section>

    <!-- Filtered Results -->
    <section class="max-w-6xl mx-auto w-full">
      <h2 class="text-2xl font-spacegrotesk font-bold mb-4">
        Showing {{ filtered.length }} {{ filtered.length === 1 ? 'Career' : 'Careers' }}
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link
          v-for="career in filtered"
          :key="career.id"
          :to="`/careers/${career.id}`"
          class="p-4 rounded-xl border shadow-md transition-all duration-200 hover:scale-[1.02] hover:shadow-lg flex flex-col justify-between"
          :style="{
            backgroundColor: 'var(--bg-color)',
            borderColor: 'var(--accent-green)',
            color: 'var(--text-color)'
          }"
        >
          <span
            class="text-xs font-semibold px-2 py-0.5 rounded-full self-start"
            :style="{ backgroundColor: 'var(--accent-blue)', color: 'var(--bg-color)' }"
          >
            {{ career.sector?.name || 'N/A' }}
          </span>
          <h3 class="text-xl font-spacegrotesk font-bold mt-2 mb-1" :style="{ color: 'var(--accent-cyan)' }">
            {{ career.name }}
          </h3>
          <p class="text-sm opacity-70 line-clamp-2">{{ career.overview }}</p>
          <p class="mt-2 text-sm">Est. Salary: R{{ career.average_salary ? career.average_salary.toLocaleString() : 'N/A' }}</p>
          <p class="text-xs opacity-80 mt-1">
            Duration: {{ career.introduction?.education_duration_years || '?' }} Years
          </p>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCareers } from '@/api/careerService'
import { getSectors } from '@/api/sectorService'

const sectors = ref([])
const careers = ref([])
const filtered = ref([])

const duration = ref(8)
const salary = ref('')
const sector = ref('')

const fetchAllData = async () => {
  try {
    const [careersRes, sectorsRes] = await Promise.all([
      getCareers(),
      getSectors()
    ])
    careers.value = careersRes.data
    sectors.value = sectorsRes.data
    applyFilters()
  } catch (err) {
    console.error('API Fetch Error:', err.response?.data || err.message)
  }
}

function applyFilters() {
  filtered.value = careers.value.filter(career => {
    const durationOk = (career.introduction?.education_duration_years || 99) <= duration.value
    const salaryOk = !salary.value || Number(career.average_salary) >= Number(salary.value)
    const sectorOk = !sector.value || career.sector?.id === sector.value
    return durationOk && salaryOk && sectorOk
  })
}

onMounted(fetchAllData)
</script>


<style scoped>
/* Added line clamp utility for cleaner cards */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
