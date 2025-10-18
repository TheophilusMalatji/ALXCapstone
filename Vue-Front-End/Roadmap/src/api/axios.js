// src/api/axios.js
import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    // Add Authorization if needed: Authorization: `Bearer ${token}`
  }
})
