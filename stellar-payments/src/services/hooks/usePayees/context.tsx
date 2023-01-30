import { createContext, useCallback, useState } from 'react'

import { AuthService } from 'app/core/auth/auth-service'
import { http } from 'interfaces/http'

import { usePayment } from '../usePayment'

export const PayeesContext = createContext(
  {} as Hooks.UsePayeesTypes.IPayeesContext
)

export const PayeesProvider: React.FC = ({ children }) => {
  const [payees, setPayees] = useState<Hooks.UsePayeesTypes.IPayee[]>()
  const [loading, setLoading] = useState(true)
  const { getPendingSigners } = usePayment()

  const getPayees = useCallback(async (): Promise<
    Hooks.UsePayeesTypes.IPayee[] | undefined
  > => {
    setLoading(true)
    try {
      const response = await http.get(`/api/payments/payees`)
      const data = response.data as Hooks.UsePayeesTypes.IPayee[]
      data.map(item => {
        item.payments = getPendingSigners(
          AuthService.currentUser().email,
          item.name
        )
      })
      setPayees(response.data)
      return response.data
    } catch (error) {
      throw new Error('Request failed')
    } finally {
      setLoading(false)
    }
  }, [getPendingSigners])

  return (
    <PayeesContext.Provider
      value={{
        getPayees,
        loading,
        payees,
      }}
    >
      {children}
    </PayeesContext.Provider>
  )
}
