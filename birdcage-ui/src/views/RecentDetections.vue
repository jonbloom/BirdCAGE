<template lang="pug">
h1 Recent Detections
ul
  b-table(:items="detections" :loading="loading")
</template>

<script setup>
import { useDetectionsStore } from '../stores/detections'
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'

const store = useDetectionsStore();
const { detections, loading } = storeToRefs(store);

onMounted(() => {
  store.fetchRecentDetections()
})
</script>