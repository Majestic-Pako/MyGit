<template>
  <section class="view history-view">
    <header class="history-header">
      <div class="history-header-copy">
        <h1>Historial</h1>

        <p>Perfiles consultados recientemente por <strong class="user-name">{{ localUser }}</strong></p>
        <span>Seleccioná un perfil para volver a abrirlo en el dashboard.</span>
      </div>

      <button v-if="history.length" type="button" class="history-clear-button"
        title="Limpiar historial" aria-label="Limpiar historial" @click="clearHistory">
        <Trash2 :size="18" aria-hidden="true" />
      </button>
    </header>

    <article v-if="!history.length" class="empty-history">
      <h2>Todavía no hay búsquedas guardadas</h2>
      <p>Cuando analices un perfil, aparecerá acá para abrirlo rápido.</p>
    </article>

    <ul v-if="history.length" class="history-list">
      <li v-for="item in history" :key="item.username" class="history-item">
        <button type="button" class="history-item-button" @click="openSearch(item.username)">
          <span class="history-user">@{{ item.username }}</span>
          <span class="history-date">{{ formatDate(item.searched_at) }}</span>
          <strong class="history-source">{{ sourceLabel(item.source) }}</strong>
          <span class="history-open">Ver dashboard →</span>
        </button>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { Trash2 } from 'lucide-vue-next'
import { useHistoryViewModel } from '../viewModels/useHistoryViewModel'
import '../css/History.css'

const { localUser, history, clearHistory, openSearch, formatDate, sourceLabel } = useHistoryViewModel()
</script>
