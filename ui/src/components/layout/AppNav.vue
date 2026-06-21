<template>
  <nav class="app-nav" aria-label="Navegación principal">
    <RouterLink to="/dashboard" class="nav-link">
      <House :size="17" :stroke-width="2.3" />
      <span>Dashboard</span>
    </RouterLink>

    <RouterLink to="/history" class="nav-link">
      <Archive :size="17" :stroke-width="2.3" />
      <span>Historial</span>
    </RouterLink>

    <button type="button" class="nav-link nav-button" @click="logout">
      <LogOut :size="17" :stroke-width="2.3" />
      <span>Salir</span>
    </button>
  </nav>
</template>

<script setup>
import { Archive, House, LogOut } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { logoutLocalUser } from '../../services/localAuthService'

const router = useRouter()

function logout() {
  logoutLocalUser()
  router.replace('/login')
}
</script>
