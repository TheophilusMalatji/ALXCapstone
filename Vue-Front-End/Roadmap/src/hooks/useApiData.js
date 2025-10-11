// src/hooks/useApiData.js
import { ref } from 'vue'

const API_BASE = 'http://localhost:2500' // JSON Server

export function useApiData() {
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchData = async (endpoint) => {
    loading.value = true
    error.value = null

    try {
      const res = await fetch(`${API_BASE}${endpoint}`)
      if (!res.ok) throw new Error(`Failed to fetch ${endpoint}`)

      const result = await res.json()

      // 🧠 Handle nested lookups automatically
      if (endpoint.startsWith('/careers/')) {
        const career = result
        const roadmapRes = await fetch(`${API_BASE}/roadmaps?career_id=${career.id}`)
        const roadmapData = await roadmapRes.json()

        if (roadmapData.length) {
          const roadmap = roadmapData[0]

          const [eduRes, skillRes, specRes] = await Promise.all([
            fetch(`${API_BASE}/education`),
            fetch(`${API_BASE}/skills`),
            fetch(`${API_BASE}/specializations`)
          ])

          const [edu, skills, specs] = await Promise.all([
            eduRes.json(),
            skillRes.json(),
            specRes.json()
          ])

          // Filter related by IDs
          roadmap.education = edu.filter(e => roadmap.education_ids.includes(e.id))
          roadmap.skills = skills.filter(s => roadmap.skill_ids.includes(s.id))
          roadmap.specializations = specs.filter(sp => roadmap.specialization_ids.includes(sp.id))

          career.roadmap = roadmap
        }

        data.value = career
      } else {
        data.value = result
      }
    } catch (err) {
      console.error(err)
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, fetchData }
}
