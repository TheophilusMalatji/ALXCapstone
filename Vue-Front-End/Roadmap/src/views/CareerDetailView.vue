<template>
  <div class="flex flex-col flex-grow p-8 space-y-8"
       :style="{ backgroundColor: 'var(--card-color)', color: 'var(--text-color)' }">

    <!-- Header -->
    <header class="border-b pb-6 max-w-5xl mx-auto">
      <h1 class="text-4xl font-spacegrotesk font-bold mb-2" :style="{ color: 'var(--accent-cyan)' }">
        {{ career?.name }}
      </h1>
      <p class="opacity-80 text-lg">{{ career?.overview }}</p>

      <div class="mt-4 flex flex-wrap gap-4 text-sm">
        <span class="px-3 py-1 rounded bg-[var(--accent-blue)]/20 text-[var(--accent-blue)] font-semibold">
          {{ sector?.name }}
        </span>
        <span class="px-3 py-1 rounded bg-[var(--accent-green)]/20 text-[var(--accent-green)] font-semibold">
          {{ career?.duration_years }} years study
        </span>
        <span class="px-3 py-1 rounded bg-[var(--accent-cyan)]/20 text-[var(--accent-cyan)] font-semibold">
          R{{ Number(career?.average_salary || 0).toLocaleString() }}
        </span>
      </div>
    </header>

    <!-- Main Grid -->
    <section class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">

      <!-- Left Column: Core Skills -->
      <div class="p-6 rounded-xl border shadow-md lg:col-span-1"
           :style="{ backgroundColor: 'var(--bg-color)', borderColor: 'var(--accent-blue)' }">
        <h2 class="text-xl font-spacegrotesk font-semibold mb-4"
            :style="{ color: 'var(--accent-green)' }">
          Core Skills
        </h2>
        <ul class="space-y-2 text-sm opacity-90">
          <li v-for="skill in skills" :key="skill.id">
            <span :style="{ color: 'var(--accent-green)' }">•</span> {{ skill.name }}
          </li>
        </ul>
      </div>

      <!-- Right Column: Education & Specialization Roadmap -->
      <div class="p-6 rounded-xl border shadow-md lg:col-span-2"
           :style="{ backgroundColor: 'var(--bg-color)', borderColor: 'var(--accent-blue)' }">
        <h2 class="text-xl font-spacegrotesk font-semibold mb-6 flex items-center"
            :style="{ color: 'var(--accent-cyan)' }">
          <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5A2.5 2.5 0 005 7.5c0 1.378.86 2.5 2 3.007V15M12 6.253c1.168.173 2.754.524 4.5 1.272A7.497 7.497 0 0119 12.5c0 1.515-.747 2.748-1.574 3.376"/>
          </svg>
          Education & Specialization Roadmap
        </h2>

        <div class="timeline">
          <div v-for="(step, index) in roadmapSteps" :key="index" class="timeline-item">
            <h4 class="text-lg font-semibold" :style="{ color: step.color }">{{ step.title }}</h4>
            <p class="text-sm opacity-80 mt-1">{{ step.details }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <div class="mt-8 pt-6 border-t text-center" :style="{ borderColor: 'var(--accent-cyan)' }">
      <router-link to="/careers"
                   class="inline-flex items-center px-6 py-3 rounded-full font-bold transition-all duration-300"
                   :style="{ backgroundColor: 'var(--accent-green)', color: 'var(--bg-color)', boxShadow: '0 0 10px var(--accent-green)' }">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to All Careers
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const career = ref(null)
const sector = ref(null)
const skills = ref([])
const roadmapSteps = ref([])

onMounted(async () => {
  const id = route.params.id

  // Fetch career
  career.value = await fetch(`http://localhost:2500/careers/${id}`).then(r => r.json())

  // Fetch sector
  sector.value = await fetch(`http://localhost:2500/sectors/${career.value.sector_id}`).then(r => r.json())

  // Fetch roadmap for this career
  const roadmap = await fetch(`http://localhost:2500/roadmaps?career_id=${id}`).then(r => r.json())
  if (roadmap.length > 0) {
    const rmap = roadmap[0]

    // Fetch related education
    const edu = await Promise.all(
      (rmap.education_ids || []).map(eid =>
        fetch(`http://localhost:2500/education/${eid}`).then(r => r.json())
      )
    )

    // Fetch related specializations
    const specs = await Promise.all(
      (rmap.specialization_ids || []).map(sid =>
        fetch(`http://localhost:2500/specializations/${sid}`).then(r => r.json())
      )
    )

    roadmapSteps.value = [
      ...edu.map(e => ({
        title: e.name,
        details: e.description,
        color: 'var(--accent-blue)'
      })),
      ...specs.map(s => ({
        title: s.name,
        details: s.description,
        color: 'var(--accent-cyan)'
      })),
    ]
  }

  // Fetch skills
  const allSkills = await fetch(`http://localhost:2500/skills`).then(r => r.json())
  skills.value = allSkills.filter(s => s.career_ids?.includes(id))
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
