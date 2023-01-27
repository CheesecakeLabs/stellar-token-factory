import { LOCAL_STORAGE_PREFIX } from 'services/utils/constants'

import { AuthService } from './auth-service'

const AUTHENTICATED = `${LOCAL_STORAGE_PREFIX}/authenticated`

export enum AuthStatus {
  Authenticated,
  Unauthenticated,
}

const logout = (): void => {
  sessionStorage.removeItem(AUTHENTICATED)
  AuthService.clearCurrentUser()
}

const setAuthenticated = (authStatus: AuthStatus): void => {
  sessionStorage.setItem(AUTHENTICATED, AuthStatus[authStatus])
}

const isAuthenticated = (): boolean => {
  return (
    sessionStorage.getItem(AUTHENTICATED) ==
    AuthStatus[AuthStatus.Authenticated]
  )
}

const Authentication = {
  isAuthenticated,
  logout,
  setAuthenticated,
}

export { Authentication }
