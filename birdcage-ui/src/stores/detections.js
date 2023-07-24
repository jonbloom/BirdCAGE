import { ref } from 'vue'
import { defineStore } from 'pinia'
import useBirdCageAPI from '../services/birdcage'

export const useDetectionsStore = defineStore('detections', () => {
  const detections = ref([])
  const fetchRecentDetections = async () => {
    const response = await useBirdCageAPI.get('/api/v2/detections/recent/10')
    detections.value = response.data
  }

  return { detections, fetchRecentDetections }
})
