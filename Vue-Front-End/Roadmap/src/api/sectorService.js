import { api } from './axios'

export const getSectors = () => api.get('/sectors/')
