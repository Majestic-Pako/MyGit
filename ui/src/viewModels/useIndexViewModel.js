import { useRouter } from 'vue-router'

export function useIndexViewModel() {
  const router = useRouter()

  const analysisSteps = [
    { event: 'profile.loaded', meta: '@octocat' },
    { event: 'repos.scanned', meta: '48 public repos' },
    { event: 'languages.detected', meta: 'Vue / TypeScript / Python' },
    { event: 'activity.processed', meta: 'recent commits' },
    { event: 'dashboard.ready', meta: 'metrics available' },
  ]

  const terminalStats = [
    { label: 'Public Repos', value: '48' },
    { label: 'Languages', value: '12' },
    { label: 'Recent Activity', value: '92%' },
    { label: 'Stars', value: '1.8k' },
  ]

  const analysisModules = [
    {
      variant: 'scan',
      tag: 'scan:user_profile',
      title: 'Perfil publico',
      description: 'Datos basicos del usuario, bio, seguidores y repos publicos.',
      icon: 'UserRound',
      status: 'status: ready',
    },
    {
      variant: 'output',
      tag: 'output:repositories',
      title: 'Repositorios',
      description: 'Proyectos publicos, estrellas, forks y ultima actualizacion.',
      icon: 'FolderGit2',
      status: 'status: ready',
    },
    {
      variant: 'scan',
      tag: 'scan:languages',
      title: 'Lenguajes',
      description: 'Tecnologias principales y distribucion del stack.',
      icon: 'Code2',
      status: 'status: ready',
    },
    {
      variant: 'output',
      tag: 'output:activity',
      title: 'Actividad',
      description: 'Senales recientes, repos activos e historial de busquedas.',
      icon: 'Activity',
      status: 'status: ready',
    },
  ]

  function goToLogin() {
    router.push('/login')
  }

  return {
    analysisModules,
    analysisSteps,
    goToLogin,
    terminalStats,
  }
}
