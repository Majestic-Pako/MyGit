import { useRouter } from 'vue-router'

export function useIndexViewModel() {
  const router = useRouter()

  function goToLogin() {
    router.push('/login')
  }

  return {
    goToLogin,
  }
}
