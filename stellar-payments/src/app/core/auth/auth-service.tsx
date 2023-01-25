import { LOCAL_STORAGE_PREFIX } from 'services/utils/constants'

const USER = `${LOCAL_STORAGE_PREFIX}/current-user`

const currentUser = (): Hooks.UseAccountTypes.IUser => {
  const user = localStorage.getItem(USER)
  return user ? JSON.parse(user) : {}
}

const setCurrentUser = (user: Hooks.UseAccountTypes.IUser): void => {
  localStorage.setItem(USER, JSON.stringify(user))
}

const clearCurrentUser = (): void => {
  localStorage.removeItem(USER)
}

const AuthService = {
  currentUser,
  setCurrentUser,
  clearCurrentUser,
}

export { AuthService }
