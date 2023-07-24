import { createRouter, createWebHistory } from 'vue-router'
import StreamsListView from '../views/StreamsList.vue'
import RecentDetectionsView from "../views/RecentDetections.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/streams',
      name: 'streams',
      component: StreamsListView
    },
    {
      path: '/recent-detections',
      name: 'recent-detections',
      component: RecentDetectionsView
    }
  ]
})

export default router
