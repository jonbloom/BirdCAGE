<template lang="pug">
h1 Streams
ul
  b-table(:items="streams" :fields="fields")
</template>

<script setup>
import { useStreamsStore } from '../stores/streams'
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'

const store = useStreamsStore();
const { streams } = storeToRefs(store);
const fields = [
  "id",
  "name",
  "protocol",
  "address",
  "transport"
];

onMounted(() => {
  store.fetchStreams()
})
</script>