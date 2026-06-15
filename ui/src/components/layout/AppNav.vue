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
  </nav>
</template>

<script setup>
import { Archive, House } from 'lucide-vue-next'
</script>