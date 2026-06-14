const HISTORY_KEY = 'mygit_search_history'

function normalizeValue(value) {
  return String(value || '').trim().toLowerCase()
}

function readHistoryStore() {
  try {
    const data = JSON.parse(localStorage.getItem(HISTORY_KEY) || '{}')
    return data && typeof data === 'object' && !Array.isArray(data) ? data : {}
  } catch {
    return {}
  }
}

function writeHistoryStore(historyStore) {
  localStorage.setItem(HISTORY_KEY, JSON.stringify(historyStore))
}

function userHistoryKey(localUser) {
  return normalizeValue(localUser)
}

export function saveSearchHistory(localUser, searchData) {
  const historyKey = userHistoryKey(localUser)
  const searchedUsername = normalizeValue(searchData.username || '')

  if (!historyKey || !searchedUsername) {
    return []
  }

  const historyStore = readHistoryStore()
  const currentHistory = Array.isArray(historyStore[historyKey])
    ? historyStore[historyKey]
    : []
  const nextEntry = {
    username: searchedUsername,
    searched_at: new Date().toISOString(),
    source: searchData.source || 'github',
    cached_at: searchData.cached_at || null,
  }

  historyStore[historyKey] = [
    nextEntry,
    ...currentHistory.filter((item) => normalizeValue(item.username || '') !== searchedUsername),
  ]

  writeHistoryStore(historyStore)
  return historyStore[historyKey]
}

export function listSearchHistory(localUser) {
  const historyStore = readHistoryStore()
  const history = historyStore[userHistoryKey(localUser)]

  return Array.isArray(history) ? history : []
}

export function clearSearchHistory(localUser) {
  const historyStore = readHistoryStore()
  delete historyStore[userHistoryKey(localUser)]
  writeHistoryStore(historyStore)
}
