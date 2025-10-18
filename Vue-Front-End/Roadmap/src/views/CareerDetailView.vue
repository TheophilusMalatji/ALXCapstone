<!--views/CareerDetailView.vue-->
<template>
  <div
    class="flex flex-col flex-grow p-8 space-y-8"
    :style="{ backgroundColor: 'var(--card-color)', color: 'var(--text-color)' }"
  >
    <div v-if="loading" class="text-center p-10">
      <div
        class="animate-spin rounded-full h-12 w-12 border-b-2"
        :style="{ borderColor: 'var(--accent-cyan)' }"
      ></div>
      <p class="mt-4">Loading career data...</p>
    </div>

    <div v-else-if="error" class="text-center p-10 text-red-500">
      <p>Error loading career: {{ error }}</p>
      <p>Check the API endpoint and ID: {{ route.params.id }}</p>
    </div>

    <div v-else-if="career" class="max-w-5xl mx-auto w-full space-y-12">
      <!-- Header -->
      <header class="border-b pb-6">
        <h1
          class="text-4xl font-spacegrotesk font-bold mb-2"
          :style="{ color: 'var(--accent-cyan)' }"
        >
          {{ career.name }}
        </h1>
        <p class="opacity-80 text-lg">{{ career.overview }}</p>

        <div class="mt-4 flex flex-wrap gap-4 text-sm">
          <span
            class="px-3 py-1 rounded bg-[var(--accent-blue)]/20 text-[var(--accent-blue)] font-semibold"
          >
            {{ career.sector?.name || 'Sector N/A' }}
          </span>
          <span
            class="px-3 py-1 rounded bg-[var(--accent-green)]/20 text-[var(--accent-green)] font-semibold"
          >
            Avg. Salary:
            R{{ career.average_salary ? career.average_salary.toLocaleString() : 'N/A' }}
          </span>
          <span
            class="px-3 py-1 rounded bg-[var(--accent-cyan)]/20 text-[var(--accent-cyan)] font-semibold"
          >
            Study Duration: {{ career.introduction?.education_duration_years || '?' }} Years
          </span>
        </div>
      </header>

      <!-- Introduction -->
      <section class="space-y-4">
        <h2 class="text-3xl font-spacegrotesk font-bold">Introduction</h2>
        <p class="opacity-90 leading-relaxed">
          {{ career.introduction?.content || 'No detailed introduction available.' }}
        </p>
      </section>

      <!-- Responsibilities -->
      <section class="space-y-4">
        <h2 class="text-3xl font-spacegrotesk font-bold">Core Responsibilities</h2>
        <ul class="list-disc list-inside space-y-2 opacity-90 ml-4">
          <li v-for="resp in career.responsibilities" :key="resp.id">
            <span class="font-semibold">{{ resp.name }}:</span> {{ resp.description }}
          </li>
        </ul>
        <p
          v-if="!career.responsibilities || career.responsibilities.length === 0"
          class="opacity-70"
        >
          No defined responsibilities.
        </p>
      </section>

      <!-- Roadmap Section Full Width -->
      <section class="max-w-6xl mx-auto grid grid-cols-1 gap-8">
        <div
          class="p-6 rounded-xl border shadow-md"
          :style="{ backgroundColor: 'var(--bg-color)', borderColor: 'var(--accent-blue)' }"
        >
          <h2
            class="text-xl font-spacegrotesk font-semibold mb-6 flex items-center"
            :style="{ color: 'var(--accent-cyan)' }"
          >
            <svg
              class="w-6 h-6 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5A2.5 2.5 0 005 7.5c0 1.378.86 2.5 2 3.007V15M12 6.253c1.168.173 2.754.524 4.5 1.272A7.497 7.497 0 0119 12.5c0 1.515-.747 2.748-1.574 3.376"
              />
            </svg>
            Career Roadmap (Education & Specialization)
          </h2>
          <div class="timeline">
            <div
              v-for="(step, index) in roadmapSteps"
              :key="index"
              class="timeline-item"
            >
              <h4 class="text-lg font-semibold" :style="{ color: step.color }">
                {{ step.title }}
              </h4>
              <p class="text-sm opacity-80 mt-1">{{ step.details }}</p>
            </div>
            <p v-if="roadmapSteps.length === 0" class="opacity-70 mt-4">
              No defined roadmap steps.
            </p>
          </div>
        </div>
      </section>

      <!-- Specializations -->
      <section class="space-y-4">
        <h2 class="text-3xl font-spacegrotesk font-bold">Specializations</h2>
        <div class="flex flex-wrap gap-4">
          <div
            v-for="spec in career.specializations"
            :key="spec.id"
            class="p-3 rounded-lg border shadow-sm max-w-sm"
            :style="{ borderColor: 'var(--accent-cyan)', backgroundColor: 'var(--bg-color)' }"
          >
            <h4 class="font-semibold" :style="{ color: 'var(--accent-cyan)' }">
              {{ spec.name }}
            </h4>
            <p class="text-sm opacity-80">{{ spec.description }}</p>
          </div>
        </div>
        <p
          v-if="!career.specializations || career.specializations.length === 0"
          class="opacity-70"
        >
          No defined specializations.
        </p>
      </section>

      <!-- Back to Careers Button -->
      <div class="mt-8 pt-6 border-t text-center" :style="{ borderColor: 'var(--accent-cyan)' }">
        <router-link
          to="/careers"
          class="inline-flex items-center px-6 py-3 rounded-full font-bold transition-all duration-300"
          :style="{
            backgroundColor: 'var(--accent-green)',
            color: 'var(--bg-color)',
            boxShadow: '0 0 10px var(--accent-green)'
          }"
        >
          <svg
            class="w-5 h-5 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M10 19l-7-7m0 0l7-7m-7 7h18"
            />
          </svg>
          Back to All Careers
        </router-link>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { getCareerById } from '@/api/careerService'

const route = useRoute()
const career = ref(null)
const loading = ref(true)
const error = ref(null)

const fetchCareerDetails = async () => {
  try {
    loading.value = true
    const response = await getCareerById(route.params.id)
    career.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || err.message
    console.error('Error fetching career details:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchCareerDetails)

// Computed roadmap for timeline
const roadmapSteps = computed(() => {
  const roadmap = career.value?.roadmap
  if (!roadmap) return []

  let steps = []
  roadmap.phases?.forEach(phase => {
    steps.push({
      title: phase.name,
      details: phase.description,
      color: 'var(--accent-blue)'
    })

    phase.required_education?.forEach(edu => {
      steps.push({
        title: `Education: ${edu.name}`,
        details: edu.description,
        color: 'var(--accent-green)'
      })
    })

    phase.required_skills?.forEach(skill => {
      steps.push({
        title: `Skill: ${skill.name}`,
        details: skill.description,
        color: 'var(--accent-cyan)'
      })
    })

    phase.required_specializations?.forEach(spec => {
      steps.push({
        title: `Specialization: ${spec.name}`,
        details: spec.description,
        color: 'var(--accent-purple)'
      })
    })
  })

  return steps
})
</script>


<style scoped>
/* Timeline styling */
.timeline {
  position: relative;
  padding-left: 25px;
}
.timeline:before {
  content: '';
  position: absolute;
  top: 0;
  left: 8px;
  bottom: 0;
  width: 2px;
  background-color: var(--accent-blue);
  opacity: 0.7;
}
.timeline-item {
  position: relative;
  margin-bottom: 2rem;
  padding-left: 30px;
}
.timeline-item:before {
  content: '';
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: var(--accent-cyan);
  border: 2px solid var(--accent-blue);
  left: 3px;
  top: 5px;
}
</style>
