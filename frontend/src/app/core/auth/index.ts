const LOCAL_STORAGE_PREFIX = '@token-factory/'
const AUTHENTICATED = `${LOCAL_STORAGE_PREFIX}authenticated`

export enum AuthStatus {
  Authenticated,
  Unauthenticated,
}

const login = async (email: string, password: string): Promise<boolean> => {
  return (
    email == process.env.REACT_APP_USERNAME &&
    password == process.env.REACT_APP_PASSWORD
  )
}

const logout = (): void => {
  localStorage.removeItem(AUTHENTICATED)
}

const setAuthenticated = (authStatus: AuthStatus): void => {
  localStorage.setItem(AUTHENTICATED, AuthStatus[authStatus])
}

const isAuthenticated = (): boolean => {
  return (
    localStorage.getItem(AUTHENTICATED) == AuthStatus[AuthStatus.Authenticated]
  )
}

const Authentication = {
  isAuthenticated,
  login,
  logout,
  setAuthenticated,
}

export { Authentication }
