<template>
  <nav
    class="sidebar flex flex-col p-6 sticky top-0 h-screen z-20 shadow-2xl transition-all duration-300"
    :style="{
      backgroundColor: 'var(--card-color)',
      color: 'var(--text-color)',
      borderRight: '1px solid var(--accent-blue)',
      boxShadow: '0 0 15px rgba(59,130,246,0.2)'
    }"
  >
    <!-- Logo -->
    <div class="mb-10 pt-2">
      <h1
        class="text-2xl md:text-3xl font-spacegrotesk font-bold tracking-tight flex items-center drop-shadow-[0_0_8px_var(--accent-cyan)]"
        :style="{ color: 'var(--accent-cyan)' }"
      >
        <svg
          class="w-7 h-7 mr-3 drop-shadow-[0_0_8px_var(--accent-blue)]"
          :style="{ color: 'var(--accent-blue)' }"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10 20l4-16m4 4v4m0 0l-4 4m-4-4v4m0 0l-4 4m-4-4l4-4m-4 4l4-4m4-4l4-4m-4 4l4 4"
          />
        </svg>
        Quantum Pathways
      </h1>
    </div>

    <!-- Navigation Links -->
    <div class="flex flex-col space-y-3 flex-grow">
      <router-link
        to="/"
        class="flex items-center space-x-3 p-3 rounded-lg transition-all duration-200"
        :class="linkClass('/')"
      >
        <svg
          class="w-5 h-5"
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
            d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3"
          />
        </svg>
        <span>Home</span>
      </router-link>

      <router-link
        to="/filter"
        class="flex items-center space-x-3 p-3 rounded-lg transition-all duration-200"
        :class="linkClass('/filter')"
      >
        <svg
          class="w-5 h-5"
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
            d="M16 8v8m-4-4v4m-4-4v4m6-10H6a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2z"
          />
        </svg>
        <span>Pathways Filter</span>
      </router-link>

      <router-link
        to="/careers"
        class="flex items-center space-x-3 p-3 rounded-lg transition-all duration-200"
        :class="linkClass('/careers')"
      >
        <svg
          class="w-5 h-5"
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
            d="M4 6h16M4 10h16M4 14h16M4 18h16"
          />
        </svg>
        <span>All Career Profiles</span>
      </router-link>
    </div>

    <!-- Theme Toggle -->
    <div class="mt-auto pt-6 border-t" :style="{ borderColor: 'var(--accent-blue)' }">
      <button
        @click="toggleTheme"
        class="w-full flex items-center justify-between p-3 rounded-lg transition-all duration-200 border"
        :style="{
          backgroundColor: 'var(--bg-color)',
          color: 'var(--text-color)',
          borderColor: 'var(--accent-blue)'
        }"
      >
        <span class="text-sm md:text-lg font-medium">Toggle Theme</span>
        <div class="flex items-center">
          <svg
            v-if="isDark"
            class="w-6 h-6 text-yellow-300"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
            />
          </svg>
          <svg
            v-else
            class="w-6 h-6"
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
              d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
            />
          </svg>
        </div>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isDark = ref(true)

const linkClass = (path) => {
  const active = route.path === path
  return active
    ? 'font-semibold border-l-4 pl-2 transition-all'
    : 'hover:bg-accent-blue/20 hover:text-accent-cyan'
}

const updateHtmlClass = (dark) => {
  const html = document.documentElement
  if (dark) html.classList.add('dark')
  else html.classList.remove('dark')
}

const toggleTheme = () => {
  isDark.value = !isDark.value
  updateHtmlClass(isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

onMounted(() => {
  const saved = localStorage.getItem('theme')
  isDark.value = saved !== 'light'
  updateHtmlClass(isDark.value)
})
</script>

<style scoped>
.sidebar {
  width: 280px;
  transition: all 0.3s ease;
}
</style>
