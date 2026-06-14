const LOCAL_USER_KEY = 'mygit_local_user'

export function saveLocalUser(username) {
  const cleanUsername = username.trim()

  if (!cleanUsername) {
    throw new Error('Ingresa un nombre para continuar.')
  }

  localStorage.setItem(LOCAL_USER_KEY, cleanUsername)
  return cleanUsername
}

export function getLocalUser() {
  return localStorage.getItem(LOCAL_USER_KEY) || ''
}

export function hasLocalSession() {
  return Boolean(getLocalUser())
}

export function clearLocalUser() {
  localStorage.removeItem(LOCAL_USER_KEY)
}

export function logoutLocalUser() {
  clearLocalUser()
}
