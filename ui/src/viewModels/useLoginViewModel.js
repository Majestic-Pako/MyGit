import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login, register } from '../services/authService'
import { saveLocalUser } from '../services/localAuthService'

export function useLoginViewModel() {
  const router = useRouter()
  const localUsername = ref('')
  const password = ref('')
  const confirmPassword = ref('')
  const isRegisterMode = ref(false)
  const loading = ref(false)
  const error = ref('')

  function toggleMode() {
    isRegisterMode.value = !isRegisterMode.value
    error.value = ''
    password.value = ''
    confirmPassword.value = ''
  }

  async function submitLogin() {
    error.value = ''

    if (!localUsername.value.trim()) {
      error.value = 'El usuario es obligatorio.'
      return
    }

    if (!password.value) {
      error.value = 'La contraseña es obligatoria.'
      return
    }

    if (isRegisterMode.value && password.value !== confirmPassword.value) {
      error.value = 'Las contraseñas no coinciden.'
      return
    }

    try {
      loading.value = true
      const authAction = isRegisterMode.value ? register : login
      const user = await authAction(localUsername.value.trim(), password.value)
      saveLocalUser(user)
      await router.push('/dashboard')
    } catch (err) {
      error.value = err.message || 'No se pudo completar la autenticación.'
    } finally {
      loading.value = false
    }
  }

  return {
    localUsername,
    password,
    confirmPassword,
    isRegisterMode,
    loading,
    error,
    toggleMode,
    submitLogin,
  }
}
