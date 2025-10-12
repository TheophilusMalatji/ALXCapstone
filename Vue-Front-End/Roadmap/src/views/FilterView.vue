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
          <label class="text-sm font-semibold">Maximum Study Duration (Years)</label>
          <input type="range" min="1" max="8" v-model="tempFilters.duration" class="w-full accent-[var(--accent-blue)] cursor-pointer"/>
          <span class="text-sm opacity-80">{{ tempFilters.duration }} years</span>
        </div>

        <!-- Salary -->
        <div class="flex flex-col space-y-2">
          <label class="text-sm font-semibold">Minimum Expected Salary (R)</label>
          <input type="number" v-model="tempFilters.salary" placeholder="e.g. 50000"
                 class="p-2 rounded border bg-transparent focus:outline-none"
                 :style="{ borderColor: 'var(--accent-blue)', color: 'var(--text-color)' }"/>
        </div>

        <!-- Sector -->
        <div class="flex flex-col space-y-2">
          <label class="text-sm font-semibold">Sector</label>
          <select v-model="tempFilters.sector" class="p-2 rounded border focus:outline-none transition-all duration-200"
                  :style="{ borderColor: 'var(--accent-blue)', backgroundColor: isDark ? '#0D1117' : '#ffffff', color: isDark ? '#ffffff' : '#000000' }">
            <option disabled value="">Select sector</option>
            <option v-for="sector in sectors" :key="sector.id" :value="sector.id">
              {{ sector.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Buttons -->
      <div class="flex justify-center mt-8 space-x-6">
        <button @click="applyFilters"
                class="px-6 py-3 rounded-full font-semibold transition-all duration-300"
                :style="{ backgroundColor: 'var(--accent-green)', color: 'var(--bg-color)', boxShadow: '0 0 10px var(--accent-green)' }">
          Apply Filters
        </button>
        <button @click="resetFilters"
                class="px-6 py-3 rounded-full font-semibold border transition-all duration-300"
                :style="{ color: 'var(--accent-cyan)', borderColor: 'var(--accent-cyan)' }">
          Reset
        </button>
      </div>
    </section>

    <!-- Results -->
    <section class="max-w-6xl mx-auto w-full">
      <h2 class="text-2xl font-spacegrotesk font-semibold mb-6 border-b pb-3"
          :style="{ color: 'var(--accent-blue)', borderColor: 'var(--accent-blue)' }">
        Matching Career Profiles
      </h2>

      <div v-if="filtered.length === 0" class="text-center text-sm opacity-70">
        No matching careers found. Try adjusting your filters.
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <router-link v-for="career in filtered" :key="career.id" :to="`/careers/${career.id}`"
                     class="p-6 rounded-xl border shadow-md hover:scale-[1.02] transition-all duration-200"
                     :style="{ backgroundColor: 'var(--bg-color)', borderColor: 'var(--accent-blue)' }">
          <h3 class="text-xl font-spacegrotesk font-bold mb-2" :style="{ color: 'var(--accent-cyan)' }">
            {{ career.name }}
          </h3>
          <p class="opacity-80 text-sm mb-4">{{ career.sector?.name }} • {{ career.duration_years }} years</p>
          <p class="opacity-70 text-sm">Est. Salary: R{{ career.average_salary.toLocaleString() }}</p>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const careers = ref([])
const sectors = ref([])

// Active filters applied on click
const filters = ref({
  sector: '',
  duration: 8,
  salary: 0
})

// Temporary values that user edits before applying
const tempFilters = ref({ ...filters.value })

const filtered = ref([])
const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches

onMounted(async () => {
  const careersData = await fetch('http://localhost:2500/careers').then(r => r.json())
  const sectorData = await fetch('http://localhost:2500/sectors').then(r => r.json())

  careers.value = careersData.map(c => ({
    ...c,
    sector: sectorData.find(s => s.id === c.sector_id)
  }))

  sectors.value = sectorData
  filtered.value = careers.value // Show all by default
})

function applyFilters() {
  filtered.value = careers.value.filter(c => {
    const matchSector = tempFilters.value.sector ? c.sector?.id === tempFilters.value.sector : true
    const matchDuration = c.duration_years <= tempFilters.value.duration
    const matchSalary = c.average_salary >= tempFilters.value.salary
    return matchSector && matchDuration && matchSalary
  })

  // Commit temp to active
  filters.value = { ...tempFilters.value }
}

function resetFilters() {
  filters.value = { sector: '', duration: 8, salary: 0 }
  tempFilters.value = { ...filters.value }
  filtered.value = careers.value
}
</script>

<style scoped>
select,
input[type='number'],
input[type='range'] {
  outline: none;
}
</style>
