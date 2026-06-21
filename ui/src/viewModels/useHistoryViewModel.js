import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getLocalUser, hasLocalSession } from '../services/localAuthService'
import {
  clearSearchHistory,
  listSearchHistory,
} from '../services/localSearchHistoryService'

export function useHistoryViewModel() {
  const router = useRouter()
  const localUser = ref('')
  const history = ref([])

  onMounted(() => {
    if (!hasLocalSession()) {
      router.replace('/login')
      return
    }

    localUser.value = getLocalUser()
    history.value = listSearchHistory(localUser.value)
  })

  function clearHistory() {
    clearSearchHistory(localUser.value)
    history.value = []
  }

  function openSearch(username) {
    router.push({
      path: '/dashboard',
      query: { username },
    })
  }

  function formatDate(dateValue) {
    return new Date(dateValue).toLocaleString()
  }

  function sourceLabel(source) {
    if (source === 'database') {
      return 'Base de datos'
    }

    if (source === 'cache') {
      return 'Cache'
    }

    if (source === 'github') {
      return 'GitHub'
    }

    return 'Origen desconocido'
  }

  return {
    localUser,
    history,
    clearHistory,
    openSearch,
    formatDate,
    sourceLabel,
  }
}
