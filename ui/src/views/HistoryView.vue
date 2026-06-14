<template>
  <section class="view">
    <h1>Historial</h1>

    <div v-if="history.length" class="history-actions">
      <p>Busquedas recientes de {{ localUser }}</p>
      <button type="button" @click="clearHistory">Limpiar historial</button>
    </div>

    <p v-else class="empty-history">Todavia no hay busquedas guardadas.</p>

    <ul v-if="history.length" class="history-list">
      <li v-for="item in history" :key="item.username" class="history-item">
        <button type="button" @click="openSearch(item.username)">
          @{{ item.username }}
        </button>
        <span>{{ formatDate(item.searched_at) }}</span>
        <strong>{{ sourceLabel(item.source) }}</strong>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { useHistoryViewModel } from '../viewModels/useHistoryViewModel'
const { localUser,history,clearHistory,openSearch,formatDate,sourceLabel,} = useHistoryViewModel()
</script>

<style scoped>
.history-actions {
  align-items: center;
  display: flex;
  gap: 16px;
  justify-content: space-between;
  margin-top: 18px;
}

.history-actions button,
.history-item button {
  border-radius: 6px;
  cursor: pointer;
  font: inherit;
}

.history-actions button {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text);
  padding: 9px 12px;
}

.empty-history {
  margin-top: 18px;
}

.history-list {
  display: grid;
  gap: 10px;
  list-style: none;
  margin: 24px 0 0;
  padding: 0;
}

.history-item {
  align-items: center;
  background: var(--surface-elevated);
  border: 1px solid var(--border);
  border-radius: 8px;
  display: grid;
  gap: 10px;
  grid-template-columns: minmax(120px, 1fr) minmax(180px, 1fr) auto;
  padding: 14px;
}

.history-item button {
  background: transparent;
  border: 0;
  color: var(--blue-soft);
  font-weight: 700;
  padding: 0;
  text-align: left;
}

.history-item span {
  color: var(--text-muted);
}

.history-item strong {
  color: var(--text-strong);
}

@media (max-width: 640px) {
  .history-actions,
  .history-item {
    align-items: flex-start;
    grid-template-columns: 1fr;
  }

  .history-actions {
    flex-direction: column;
  }
}
</style>
