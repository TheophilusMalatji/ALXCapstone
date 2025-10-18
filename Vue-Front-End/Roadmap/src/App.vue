<template>
  <div class="min-h-screen flex text-text-light bg-bg-deep">
    <!-- Sidebar -->
    <aside class="hidden md:block">
      <SidebarNav />
    </aside>

    <!-- Main content -->
    <main class="flex-1 bg-bg-deep">
      <div class="h-fulloverflow-y-auto min-h-screen">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import SidebarNav from '@/components/SidebarNav.vue'
import { ref, onMounted } from 'vue';
import axios from 'axios';

const data = ref(null);
const isLoading = ref(true);
const error = ref(null);
const fetchData = async () => {
      try {
        isLoading.value = true;
        const response = await axios.get('http://localhost:8000/api/careers');
        data.value = response.data;
      } catch (err) {
        error.value = err;
      } finally {
        isLoading.value = false;
      }
    };
onMounted(() => {
      fetchData();
      return {
      data,
      isLoading,
      error,
      fetchData, // Optional: if you want to re-fetch data manually
    };
    });

</script>

<style>
html, body, #app {
  margin: 0;
  height: 100%;
  font-family: 'Inter', sans-serif;
  background-color: #0D1117;
}

/* Color palette (preserved from your HTML) */
:root {
  --bg-deep: #161B22;
  --bg-card-dark: #161B22;
  --accent-blue: #3B82F6;
  --accent-cyan: #00FFFF;
  --text-light: #D1D5DB;
  --text-dark: #0D1117;
}

.bg-bg-deep {
  background-color: var(--bg-deep);
}

.bg-bg-card-dark {
  background-color: var(--bg-card-dark);
}

.text-text-light {
  color: var(--text-light);
}

.text-accent-blue {
  color: var(--accent-blue);
}

.text-accent-cyan {
  color: var(--accent-cyan);
}
</style>
