import { createContext, useCallback, useState } from 'react'

import { recordUsers } from 'services/utils/users'

import { Authentication, AuthStatus } from 'app/core/auth'
import { AuthService } from 'app/core/auth/auth-service'
import { http } from 'interfaces/http'

export const AccountContext = createContext(
  {} as Hooks.UseAccountTypes.IAccountContext
)

export const AccountProvider: React.FC = ({ children }) => {
  const [balance, setBalance] = useState<Hooks.UseAccountTypes.IBalance>()
  const [loading, setLoading] = useState(true)

  const getBalance = useCallback(async (): Promise<
    Hooks.UseAccountTypes.IBalance | undefined
  > => {
    setLoading(true)
    try {
      const response = await http.get(`/api/payments/balances/eur`)
      setBalance(response.data)
      return response.data
    } catch (error) {
      return undefined
    } finally {
      setLoading(false)
    }
  }, [])

  async function signIn(
    params: Hooks.UseAccountTypes.ISignIn
  ): Promise<boolean> {
    setLoading(true)

    try {
      const user = recordUsers(params.email)

      if (user) {
        Authentication.setAuthenticated(AuthStatus.Authenticated)
        AuthService.setCurrentUser(user)
      }

      return user != undefined
    } catch (error) {
      return false
    } finally {
      setLoading(false)
    }
  }

  return (
    <AccountContext.Provider
      value={{
        getBalance,
        loading,
        balance,
        signIn,
      }}
    >
      {children}
    </AccountContext.Provider>
  )
}
