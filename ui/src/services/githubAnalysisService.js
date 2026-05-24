const API_URL = import.meta.env.VITE_API_URL

export async function getGithubUser(username) {
  const cleanUsername = username.trim()

  if (!cleanUsername) {
    throw new Error('Ingresa un username de GitHub.')
  }

  if (!API_URL) {
    throw new Error('Falta configurar VITE_API_URL en ui/.env.')
  }

  try {
    const response = await fetch(`${API_URL}/github/user/${encodeURIComponent(cleanUsername)}`)

    if (!response.ok) {
      const errorData = await response.json().catch(() => null)
      throw new Error(errorData?.detail || 'No se pudo obtener el usuario de GitHub.')
    }

    return response.json()
  } catch (err) {
    if (err instanceof TypeError) {
      throw new Error('No se pudo conectar con el backend. Revisa que este activo y tenga CORS habilitado.')
    }

    throw err
  }
}
