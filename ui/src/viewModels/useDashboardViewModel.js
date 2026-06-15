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
  const normalizedRepositories = computed(() => {
    return getRepositorySources(result.value).map(normalizeRepository)
  })
  const repositoriesCount = computed(() => normalizedRepositories.value.length)
  const hasRepositories = computed(() => repositoriesCount.value > 0)
  const featuredRepositories = computed(() => {
    return [...normalizedRepositories.value]
      .sort(compareFeaturedRepositories)
      .slice(0, 6)
  })
  const languageDistribution = computed(() => {
    const languageCounts = normalizedRepositories.value.reduce((accumulator, repository) => {
      if (!repository.language || repository.language === 'Sin especificar') {
        return accumulator
      }

      accumulator.set(repository.language, (accumulator.get(repository.language) || 0) + 1)
      return accumulator
    }, new Map())
    const total = [...languageCounts.values()].reduce((sum, count) => sum + count, 0)

    if (!total) {
      return []
    }

    return [...languageCounts.entries()]
      .map(([language, count]) => ({
        language,
        count,
        percentage: Math.round((count / total) * 100),
        color: getLanguageColor(language),
      }))
      .sort((a, b) => b.count - a.count || a.language.localeCompare(b.language))
      .slice(0, 5)
  })
  const recentRepositories = computed(() => {
    return normalizedRepositories.value
      .filter((repository) => repository.updatedAt)
      .sort((a, b) => getDateTime(b.updatedAt) - getDateTime(a.updatedAt))
      .slice(0, 3)
  })
  const analysisStatus = computed(() => {
    const hasProfile = Boolean(result.value?.profile)
    const hasLanguages = languageDistribution.value.length > 0
    const hasCacheMetadata = Boolean(result.value?.metadata?.source || result.value?.metadata?.cached_at)

    return [
      {
        label: hasProfile ? '[OK] Perfil general' : '[PENDING] Perfil general',
        state: hasProfile ? 'ok' : 'pending',
      },
      {
        label: hasRepositories.value ? '[OK] Repositorios' : '[PENDING] Repositorios',
        state: hasRepositories.value ? 'ok' : 'pending',
      },
      {
        label: hasLanguages ? '[OK] Lenguajes' : '[PENDING] Lenguajes',
        state: hasLanguages ? 'ok' : 'pending',
      },
      {
        label: hasCacheMetadata ? '[READY] cache.metadata' : '[PENDING] cache.metadata',
        state: hasCacheMetadata ? 'ready' : 'pending',
      },
    ]
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

  function formatShortDate(dateValue) {
    if (!dateValue) {
      return ''
    }

    const date = new Date(dateValue)
    if (Number.isNaN(date.getTime())) {
      return ''
    }

    return date.toLocaleDateString()
  }

  return {
    localUser,
    username,
    loading,
    error,
    result,
    sourceMessage,
    normalizedRepositories,
    featuredRepositories,
    repositoriesCount,
    languageDistribution,
    recentRepositories,
    hasRepositories,
    analysisStatus,
    searchUser,
    formatDate,
    formatShortDate,
  }
}

function getRepositorySources(currentResult) {
  const candidates = [
    currentResult?.repositories,
    currentResult?.profile?.repositories,
    currentResult?.data?.repositories,
    currentResult?.analysis?.repositories,
    currentResult?.analysis?.repositories?.items,
    currentResult?.analysis?.repositories?.recently_updated,
  ]

  return candidates.find(Array.isArray) || []
}

function normalizeRepository(repository) {
  const stars = repository?.stars ?? repository?.stargazers_count ?? 0
  const forks = repository?.forks ?? repository?.forks_count ?? 0
  const updatedAt = repository?.updatedAt ?? repository?.updated_at ?? repository?.last_commit ?? null

  return {
    name: repository?.name || 'Repositorio sin nombre',
    description: repository?.description || 'Sin descripcion disponible.',
    language: repository?.language || 'Sin especificar',
    stars: Number.isFinite(Number(stars)) ? Number(stars) : 0,
    forks: Number.isFinite(Number(forks)) ? Number(forks) : 0,
    updatedAt,
    url: repository?.url ?? repository?.html_url ?? null,
    isFork: Boolean(repository?.isFork ?? repository?.is_fork ?? repository?.fork ?? false),
  }
}

function compareFeaturedRepositories(a, b) {
  if (a.isFork !== b.isFork) {
    return a.isFork ? 1 : -1
  }

  const updatedDifference = getDateTime(b.updatedAt) - getDateTime(a.updatedAt)
  if (updatedDifference) {
    return updatedDifference
  }

  return b.stars - a.stars
}

function getDateTime(dateValue) {
  if (!dateValue) {
    return 0
  }

  const time = new Date(dateValue).getTime()
  return Number.isNaN(time) ? 0 : time
}

function getLanguageColor(language) {
  const languageColors = {
    JavaScript: '#d8a657',
    Python: '#58a6ff',
    CSS: '#a78bfa',
    Java: '#f59e6c',
    PHP: '#b9a7ff',
    Vue: '#42b883',
    TypeScript: '#79c0ff',
  }

  return languageColors[language] || '#8b949e'
}
