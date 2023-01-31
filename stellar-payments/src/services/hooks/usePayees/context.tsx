import { createContext, useCallback, useState } from 'react'

import { http } from 'interfaces/http'

export const PayeesContext = createContext(
  {} as Hooks.UsePayeesTypes.IPayeesContext
)

export const PayeesProvider: React.FC = ({ children }) => {
  const [payees, setPayees] = useState<Hooks.UsePayeesTypes.IPayee[]>()
  const [loading, setLoading] = useState(true)

  const getPayees = useCallback(async (): Promise<
    Hooks.UsePayeesTypes.IPayee[] | undefined
  > => {
    setLoading(true)
    try {
      const response = await http.get(`/api/payments/payees`)
      setPayees(response.data)
      return response.data
    } catch (error) {
      throw new Error('Request failed')
    } finally {
      setLoading(false)
    }
  }, [])

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
