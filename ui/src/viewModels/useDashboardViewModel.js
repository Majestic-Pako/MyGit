import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getGithubUser } from '../services/githubAnalysisService'
import { getLocalUser, hasLocalSession } from '../services/localAuthService'
import { saveSearchHistory } from '../services/localSearchHistoryService'

export function useDashboardViewModel() {
  const route = useRoute()
  const router = useRouter()
  const localUser = ref('')
  const username = ref('')
  const loading = ref(false)
  const error = ref('')
  const result = ref(null)
  const sourceMessage = computed(() => {
    if (result.value?.metadata?.source === 'cache') {
      return 'Datos cargados desde cache'
    }

    if (result.value?.metadata?.source === 'github') {
      return 'Datos obtenidos desde GitHub'
    }

    return ''
  })

  onMounted(() => {
    if (!hasLocalSession()) {
      router.replace('/login')
      return
    }

    localUser.value = getLocalUser()

    if (typeof route.query.username === 'string') {
      username.value = route.query.username
      searchUser()
    }
  })

  async function searchUser() {
    loading.value = true
    error.value = ''
    result.value = null

    try {
      result.value = await getGithubUser(username.value)
      saveSearchHistory(localUser.value, {
        username: result.value.profile?.username || username.value,
        source: result.value.metadata?.source,
        cached_at: result.value.metadata?.cached_at,
      })
    } catch (err) {
      error.value = err.message || 'Ocurrio un error inesperado.'
    } finally {
      loading.value = false
    }
  }

  function formatDate(dateValue) {
    return new Date(dateValue).toLocaleString()
  }

  return {
    localUser,
    username,
    loading,
    error,
    result,
    sourceMessage,
    searchUser,
    formatDate,
  }
}
