const LOCAL_USER_KEY = 'mygit_local_user'
const AUTHENTICATED_USER_KEY = 'mygit_authenticated_user'

export function saveLocalUser(user) {
  const cleanUsername = (typeof user === 'string' ? user : user?.username || '').trim()

  if (!cleanUsername) {
    throw new Error('Ingresa un nombre para continuar.')
  }

  localStorage.setItem(LOCAL_USER_KEY, cleanUsername)
  if (typeof user === 'object' && user !== null) {
    localStorage.setItem(AUTHENTICATED_USER_KEY, JSON.stringify({
      id: user.id,
      username: cleanUsername,
    }))
  }
  return cleanUsername
}

export function getAuthenticatedUser() {
  try {
    return JSON.parse(localStorage.getItem(AUTHENTICATED_USER_KEY))
  } catch {
    return null
  }
}

export function getLocalUser() {
  return localStorage.getItem(LOCAL_USER_KEY) || ''
}

export function hasLocalSession() {
  return Boolean(getLocalUser())
}

export function clearLocalUser() {
  localStorage.removeItem(LOCAL_USER_KEY)
  localStorage.removeItem(AUTHENTICATED_USER_KEY)
}

export function logoutLocalUser() {
  clearLocalUser()
}
