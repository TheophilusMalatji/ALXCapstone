import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCareerFilters = defineStore('careerFilters', () => {
  const filters = ref({
    sector: '',
    duration: 8,
    salary: 0
  })

  const filteredCareers = ref([])

  // Optionally store all careers too for easy filtering inside the store
  const allCareers = ref([])

  function setFilters(newFilters) {
    filters.value = { ...newFilters }
  }

  function setAllCareers(careers) {
    allCareers.value = careers
    filteredCareers.value = careers
  }

  function applyFilters() {
    filteredCareers.value = allCareers.value.filter(c => {
      const matchSector = filters.value.sector ? c.sector?.id === filters.value.sector : true
      const matchDuration = c.duration_years <= filters.value.duration
      const matchSalary = c.average_salary >= filters.value.salary
      return matchSector && matchDuration && matchSalary
    })
  }

  function resetFilters() {
    filters.value = { sector: '', duration: 8, salary: 0 }
    filteredCareers.value = allCareers.value
  }

  return { filters, filteredCareers, setFilters, setAllCareers, applyFilters, resetFilters }
})
