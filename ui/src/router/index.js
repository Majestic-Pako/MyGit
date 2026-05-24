import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import HistoryView from '../views/HistoryView.vue'
import MetricsView from '../views/MetricsView.vue'
import ProfileView from '../views/ProfileView.vue'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView,
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
  },
  {
    path: '/metrics',
    name: 'metrics',
    component: MetricsView,
  },
  {
    path: '/history',
    name: 'history',
    component: HistoryView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
