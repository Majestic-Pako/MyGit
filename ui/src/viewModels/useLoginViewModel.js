import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { saveLocalUser } from '../services/localAuthService'

export function useLoginViewModel() {
  const router = useRouter()
  const localUsername = ref('')
  const error = ref('')

  function submitLogin() {
    error.value = ''

    try {
      saveLocalUser(localUsername.value)
      router.push('/dashboard')
    } catch (err) {
      error.value = err.message || 'No se pudo iniciar la sesion local.'
    }
  }

  return {
    localUsername,
    error,
    submitLogin,
  }
}
