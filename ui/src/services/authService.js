const API_URL = import.meta.env.VITE_API_URL

async function authRequest(path, username, password) {
  if (!API_URL) {
    throw new Error('Falta configurar VITE_API_URL en ui/.env.')
  }

  try {
    const response = await fetch(`${API_URL}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
    const data = await response.json().catch(() => null)

    if (!response.ok) {
      throw new Error(data?.detail || 'No se pudo completar la autenticación.')
    }

    return data
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error('No se pudo conectar con el backend. Revisá que esté activo.')
    }

    throw error
  }
}

export function register(username, password) {
  return authRequest('/auth/register', username, password)
}

export function login(username, password) {
  return authRequest('/auth/login', username, password)
}
