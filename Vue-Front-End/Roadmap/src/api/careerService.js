// src/api/careerService.js
import { api } from './axios'

export const getCareers = () => api.get('/careers/')
export const getCareerById = (id) => api.get(`/careers/${id}/`)
export const getSectors = () => api.get('/sectors/')
export const getIntroductions = () => api.get('/introductions/')
export const getSkills = () => api.get('/skills/')
export const getEducation = () => api.get('/education/')
export const getResponsibilities = () => api.get('/responsibilities/')
export const getSpecializations = () => api.get('/specializations/')
export const getRoadmaps = () => api.get('/roadmaps/')
