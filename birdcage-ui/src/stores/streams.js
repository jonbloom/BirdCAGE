import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import useBirdCageAPI from '../services/birdcage'


export const useStreamsStore = defineStore('streams', () => {
  const streams = ref([])
  const loading = ref(false)
  const fetchStreams = async () => {
    loading.value = true
    const response = await useBirdCageAPI.get('/api/streams')
    streams.value = response.data
    loading.value = false
  }


  return { streams, fetchStreams }
})
