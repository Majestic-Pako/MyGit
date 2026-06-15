<template>
  <header class="app-header">
    <RouterLink class="brand" to="/" title="Inicio">
      <span class="brand-icon">
        <Github :size="19" :stroke-width="2.4" />
      </span>
      <span class="brand-text">MyGit</span>
    </RouterLink>

    <AppNav />
  </header>
</template>

<script setup>
import { Github } from 'lucide-vue-next'
import AppNav from './AppNav.vue'
</script>