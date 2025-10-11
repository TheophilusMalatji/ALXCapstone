<template>
  <div
    class="flex flex-col flex-grow"
    :style="{ backgroundColor: 'var(--card-color)', color: 'var(--text-color)' }"
  >
    <main
      class="w-full shadow-inner p-8 flex-grow transition-all duration-300"
      :style="{
        backgroundColor: 'var(--card-color)',
        boxShadow: 'inset 0 0 30px rgba(0,0,0,0.5)',
      }"
    >
      <!-- Hero Section -->
      <section
        class="text-center py-16 px-4 mb-10 border-b max-w-5xl mx-auto transition-all duration-300"
        :style="{ borderColor: 'var(--accent-blue)' }"
      >
        <h2
          class="text-5xl md:text-6xl font-spacegrotesk font-extrabold mb-4 tracking-tighter"
          :style="{ color: 'var(--text-color)' }"
        >
          Welcome to the
          <span :style="{ color: 'var(--accent-cyan)' }">Pathfinding Console</span>
        </h2>

        <p
          class="text-xl max-w-3xl mx-auto mb-8 opacity-80"
          :style="{ color: 'var(--text-muted, #8B949E)' }"
        >
          Analyze, filter, and visualize your optimal career trajectory in the digital economy.
          Your future path starts here.
        </p>

        <router-link
          to="/filter"
          class="inline-flex items-center justify-center px-8 py-3 text-lg font-bold rounded-full transition duration-300"
          :style="{
            color: 'var(--bg-color)',
            backgroundColor: 'var(--accent-green)',
            boxShadow: '0 0 10px var(--accent-green)',
          }"
          @mouseover="hoverButton = true"
          @mouseleave="hoverButton = false"
        >
          Start Your Career Scan
          <svg
            class="w-5 h-5 ml-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
            :style="{ transform: hoverButton ? 'translateX(4px)' : 'none', transition: 'transform 0.3s ease' }"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M14 5l7 7m0 0l-7 7m7-7H3"
            ></path>
          </svg>
        </router-link>
      </section>

      <!-- System Capabilities Section -->
      <section class="max-w-5xl mx-auto">
        <h3
          class="text-3xl font-spacegrotesk font-bold mb-8 border-b pb-3"
          :style="{ color: 'var(--accent-blue)', borderColor: 'var(--accent-blue)' }"
        >
          System Capabilities
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Capability 1 -->
          <div
            class="p-6 rounded-xl border shadow-xl transition duration-200"
            :style="{
              backgroundColor: 'var(--bg-color)',
              borderColor: 'var(--accent-cyan)',
            }"
          >
            <svg
              class="w-10 h-10 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              :style="{ color: 'var(--accent-cyan)' }"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM4 10h16a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6a1 1 0 011-1z"
              />
            </svg>
            <h4 class="text-xl font-spacegrotesk font-bold mb-2">Targeted Search Protocol</h4>
            <p class="opacity-80">
              Use the Pathways Filter to narrow down careers based on required education time,
              minimum salary expectations, and preferred industry sector.
            </p>
          </div>

          <!-- Capability 2 -->
          <div
            class="p-6 rounded-xl border shadow-xl transition duration-200"
            :style="{
              backgroundColor: 'var(--bg-color)',
              borderColor: 'var(--accent-green)',
            }"
          >
            <svg
              class="w-10 h-10 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              :style="{ color: 'var(--accent-green)' }"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0zM12 2v2m0 16v2m9-9h-2M3 12H1m15.364 6.364l-1.414-1.414M6.05 6.05L4.636 4.636m12.04 0l-1.414 1.414m-12.04 12.04l1.414-1.414"
              />
            </svg>
            <h4 class="text-xl font-spacegrotesk font-bold mb-2">Detailed Trajectory Maps</h4>
            <p class="opacity-80">
              View detailed educational steps, core competencies, and specialization modules for
              each matching career profile.
            </p>
          </div>

          <!-- Capability 3 -->
          <div
            class="p-6 rounded-xl border shadow-xl transition duration-200"
            :style="{
              backgroundColor: 'var(--bg-color)',
              borderColor: 'var(--accent-blue)',
            }"
          >
            <svg
              class="w-10 h-10 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              :style="{ color: 'var(--accent-blue)' }"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m-6 0h6"
              />
            </svg>
            <h4 class="text-xl font-spacegrotesk font-bold mb-2">Outlook Projection</h4>
            <p class="opacity-80">
              Gain immediate insights into job growth projections and estimated remuneration based
              on synthesized industry data.
            </p>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
   
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue'
import { useApiData } from '@/hooks/useApiData'

const { data: careers, fetchData } = useApiData()

onMounted(async () => {
  await fetchData('/careers?_limit=2') // get 2 random careers
})

const hoverButton = ref(false)
</script>

<style scoped>
/* Ensure spacing matches original design */
main {
  font-family: 'Inter', sans-serif;
}

/* Smooth hover glow */
a:hover {
  filter: brightness(1.1);
  transition: all 0.3s ease;
}
</style>
