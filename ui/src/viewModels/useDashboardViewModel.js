import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getGithubUser } from '../services/githubAnalysisService'
import { getLocalUser, hasLocalSession } from '../services/localAuthService'
import { saveSearchHistory } from '../services/localSearchHistoryService'
import { getLanguageAccent } from '../utils/languageIcons'

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
  const languageSummary = computed(() => {
    return buildLanguageSummary(result.value?.analysis?.languages, normalizedRepositories.value)
  })
  const collaborationSummary = computed(() => {
    return buildCollaborationSummary(
      result.value?.analysis?.collaboration,
      result.value?.profile?.username,
    )
  })
  const recentRepositories = computed(() => {
    return normalizedRepositories.value
      .filter((repository) => repository.updatedAt)
      .sort((a, b) => getDateTime(b.updatedAt) - getDateTime(a.updatedAt))
      .slice(0, 3)
  })
  const analysisStatus = computed(() => {
    const hasProfile = Boolean(result.value?.profile)
    const hasLanguages = languageSummary.value.languages.length > 0
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
    languageSummary,
    collaborationSummary,
    recentRepositories,
    hasRepositories,
    analysisStatus,
    searchUser,
    formatDate,
    formatShortDate,
  }
}

function buildLanguageSummary(languageAnalysis, repositories) {
  const backendLanguages = getBackendLanguageEntries(languageAnalysis)
  const usesBackendAnalysis = backendLanguages.length > 0
  const entries = usesBackendAnalysis
    ? backendLanguages
    : getRepositoryLanguageEntries(repositories)
  const total = entries.reduce((sum, [, value]) => sum + value, 0)
  const providedPercentages = languageAnalysis?.percentages

  const languages = entries
    .map(([language, value]) => ({
      language,
      value,
      percentage: getLanguagePercentage(language, value, total, providedPercentages),
      color: getLanguageAccent(language),
    }))
    .sort((a, b) => b.value - a.value || a.language.localeCompare(b.language))

  const primaryLanguage = languageAnalysis?.primary_language || languages[0]?.language || null
  const primary = languages.find(
    (language) => language.language.toLowerCase() === String(primaryLanguage).toLowerCase(),
  ) || languages[0] || null
  const chartLanguages = groupLanguageEntries(languages)

  return {
    languages,
    chartLanguages,
    donutGradient: buildDonutGradient(chartLanguages),
    totalLanguages: languages.length,
    primary,
    primaryLanguage: primary?.language || null,
    feedback: getLanguageFeedback(primary),
    source: usesBackendAnalysis ? 'backend' : languages.length ? 'repositories' : 'empty',
  }
}

function getBackendLanguageEntries(languageAnalysis) {
  if (!languageAnalysis || typeof languageAnalysis !== 'object') {
    return []
  }

  const hasNestedLanguages = languageAnalysis.languages
    && typeof languageAnalysis.languages === 'object'
    && !Array.isArray(languageAnalysis.languages)
  const languageValues = hasNestedLanguages
    ? languageAnalysis.languages
    : languageAnalysis
  const metadataKeys = new Set([
    'primary_language', 'total_languages', 'percentages',
    'repos_per_language', 'languages_per_repo',
  ])

  return Object.entries(languageValues)
    .filter(([language, value]) => (
      language
      && !metadataKeys.has(language)
      && Number.isFinite(Number(value))
      && Number(value) > 0
    ))
    .map(([language, value]) => [language, Number(value)])
}

function getRepositoryLanguageEntries(repositories) {
  const languageCounts = repositories.reduce((counts, repository) => {
    if (repository.language && repository.language !== 'Sin especificar') {
      counts.set(repository.language, (counts.get(repository.language) || 0) + 1)
    }

    return counts
  }, new Map())

  return [...languageCounts.entries()]
}

function getLanguagePercentage(language, value, total, providedPercentages) {
  const providedValue = Number(providedPercentages?.[language])

  if (Number.isFinite(providedValue)) {
    return providedValue
  }

  return total ? Math.round((value / total) * 1000) / 10 : 0
}

function getLanguageFeedback(primaryLanguage) {
  if (!primaryLanguage) {
    return 'Todavia no hay datos de lenguajes disponibles.'
  }

  if (primaryLanguage.percentage >= 60) {
    return `El perfil esta enfocado principalmente en ${primaryLanguage.language}.`
  }

  return 'El perfil muestra variedad tecnologica entre sus lenguajes.'
}

function groupLanguageEntries(languages, visibleLimit = 6) {
  if (languages.length <= visibleLimit) {
    return languages
  }

  const visibleLanguages = languages.slice(0, visibleLimit - 1)
  const remainingLanguages = languages.slice(visibleLimit - 1)

  return [
    ...visibleLanguages,
    {
      language: 'Otros',
      value: remainingLanguages.reduce((sum, language) => sum + language.value, 0),
      percentage: remainingLanguages.reduce((sum, language) => sum + language.percentage, 0),
      color: '#64748b',
      groupedCount: remainingLanguages.length,
    },
  ]
}

function buildDonutGradient(languages) {
  const total = languages.reduce((sum, language) => sum + language.percentage, 0)
  if (!total) return 'var(--border-soft) 0 100%'

  let cursor = 0
  return languages.map((language, index) => {
    const start = cursor
    cursor += (language.percentage / total) * 100
    const end = index === languages.length - 1 ? 100 : cursor
    return `${language.color} ${start.toFixed(2)}% ${end.toFixed(2)}%`
  }).join(', ')
}

function buildCollaborationSummary(collaborationAnalysis, ownerUsername) {
  const rawContributors = Array.isArray(collaborationAnalysis?.contributors)
    ? collaborationAnalysis.contributors
    : []
  const repositoriesByContributor = getRepositoriesByContributor(collaborationAnalysis?.by_repository)
  const contributors = rawContributors
    .map((contributor) => normalizeContributor(contributor, repositoriesByContributor, ownerUsername))
    .sort(compareContributorsByFrequency)
  const totalContributions = contributors.reduce(
    (sum, contributor) => sum + contributor.contributions,
    0,
  )
  const repositoriesAnalyzed = getAnalyzedRepositoryCount(
    collaborationAnalysis?.by_repository,
    contributors,
  )
  const owner = contributors.find((contributor) => contributor.isOwner)
  const externalContributors = contributors.filter((contributor) => !contributor.isOwner)
  const maxFrequency = Math.max(...contributors.map((contributor) => contributor.repositoryCount), 0)

  contributors.forEach((contributor) => {
    contributor.frequencyPercentage = maxFrequency
      ? Math.round((contributor.repositoryCount / maxFrequency) * 100)
      : 0
  })

  const ownerFrequency = owner?.repositoryCount || 0
  const externalFrequency = externalContributors.reduce(
    (sum, contributor) => sum + contributor.repositoryCount,
    0,
  )
  const hasFrequencyData = ownerFrequency + externalFrequency > 0
  const ownerComparisonValue = hasFrequencyData ? ownerFrequency : owner?.contributions || 0
  const externalComparisonValue = hasFrequencyData
    ? externalFrequency
    : externalContributors.reduce((sum, contributor) => sum + contributor.contributions, 0)
  const comparisonTotal = ownerComparisonValue + externalComparisonValue
  const ownerPercentage = comparisonTotal
    ? Math.round((ownerComparisonValue / comparisonTotal) * 100)
    : 0

  return {
    contributors,
    totalContributors: Number(collaborationAnalysis?.total_contributors) || contributors.length,
    totalContributions,
    repositoriesAnalyzed,
    externalContributors: externalContributors.length,
    ownerUsername: owner?.username || ownerUsername || '',
    ownerPercentage,
    externalPercentage: comparisonTotal ? 100 - ownerPercentage : 0,
    comparisonBasis: hasFrequencyData ? 'apariciones en repositorios' : 'contribuciones registradas',
    hasComparisonData: comparisonTotal > 0,
    pattern: getCollaborationPattern(externalContributors, repositoriesAnalyzed),
  }
}

function getCollaborationPattern(externalContributors, repositoriesAnalyzed) {
  if (!repositoriesAnalyzed) {
    return {
      key: 'limited',
      label: 'Datos colaborativos limitados',
      feedback: 'No hay suficientes repositorios analizados para estimar un patron colaborativo.',
    }
  }

  if (!externalContributors.length) {
    return {
      key: 'independent',
      label: 'Perfil mayormente independiente',
      feedback: 'La muestra analizada no presenta contributors externos con frecuencia relevante.',
    }
  }

  if (externalContributors.some((contributor) => contributor.repositoryCount >= 2)) {
    return {
      key: 'recurrent',
      label: 'Colaboracion recurrente',
      feedback: 'Hay contributors externos que se repiten en varios repositorios de la muestra.',
    }
  }

  return {
    key: 'occasional',
    label: 'Colaboracion ocasional',
    feedback: 'Se detectaron contributors externos, aunque aparecen en pocos repositorios.',
  }
}

function getRepositoriesByContributor(byRepository) {
  const repositoriesByContributor = new Map()

  if (!Array.isArray(byRepository)) {
    return repositoriesByContributor
  }

  byRepository.forEach((repositoryData) => {
    const repositoryName = repositoryData?.repository || repositoryData?.name
    const contributors = Array.isArray(repositoryData?.contributors) ? repositoryData.contributors : []

    contributors.forEach((contributor) => {
      const username = contributor?.username || contributor?.login
      if (!username || !repositoryName) return

      const repositories = repositoriesByContributor.get(username) || new Set()
      repositories.add(repositoryName)
      repositoriesByContributor.set(username, repositories)
    })
  })

  return repositoriesByContributor
}

function normalizeContributor(contributor, repositoriesByContributor, ownerUsername) {
  const username = contributor?.username || contributor?.login || 'Contributor desconocido'
  const providedRepositories = Array.isArray(contributor?.repositories)
    ? contributor.repositories.filter(Boolean)
    : []
  const repositories = providedRepositories.length
    ? [...new Set(providedRepositories)]
    : [...(repositoriesByContributor.get(username) || [])]
  const contributions = Number(contributor?.total_contributions ?? contributor?.contributions ?? 0)

  return {
    username,
    contributions: Number.isFinite(contributions) ? contributions : 0,
    repositoryCount: repositories.length,
    repositories,
    isOwner: username.toLowerCase() === String(ownerUsername || '').toLowerCase(),
    frequencyPercentage: 0,
  }
}

function compareContributorsByFrequency(a, b) {
  return b.repositoryCount - a.repositoryCount
    || b.contributions - a.contributions
    || a.username.localeCompare(b.username)
}

function getAnalyzedRepositoryCount(byRepository, contributors) {
  const repositories = new Set()

  if (Array.isArray(byRepository)) {
    byRepository.forEach((repositoryData) => {
      const repositoryName = repositoryData?.repository || repositoryData?.name
      if (repositoryName) repositories.add(repositoryName)
    })
  }

  contributors.forEach((contributor) => {
    contributor.repositories.forEach((repository) => repositories.add(repository))
  })

  return repositories.size
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
