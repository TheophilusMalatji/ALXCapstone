// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Lazy-loaded views
const HomeView = () => import('@/views/HomeView.vue')
const FilterView = () => import('@/views/FilterView.vue')
const CareerListView = () => import('@/views/CareerListView.vue')
const ProfileView = () => import('@/views/ProfileView.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView,
    },
    {
      path: '/filter',
      name: 'Filter',
      component: FilterView,
    },
    {
      path: '/careers',
      name: 'Careers',
      component: CareerListView,
    },
    {
      path: '/profile',
      name: 'Profile',
      component: ProfileView,
    },
    {
  path: '/careers/:id',
  name: 'CareerDetail',
  component: () => import('@/views/CareerDetailView.vue')
}

  ],
  scrollBehavior() {
    return { top: 0 }
  },
  
})

export default router
