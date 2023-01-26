import { createContext, useCallback, useState } from 'react'

import { http } from 'interfaces/http'

export const PaymentContext = createContext(
  {} as Hooks.UsePaymentTypes.IPaymentContext
)

export const PaymentProvider: React.FC = ({ children }) => {
  const [payment, setPayment] = useState<Hooks.UsePaymentTypes.IPayment>()
  const [loading, setLoading] = useState(false)

  const createPayment = useCallback(
    async (
      params: Hooks.UsePaymentTypes.IPaymentParams
    ): Promise<Hooks.UsePaymentTypes.IPayment | undefined> => {
      setLoading(true)
      try {
        const response = await http.post(
          `/api/payments/path-payment-strict-receive`,
          params
        )
        setPayment(response.data)
        return response.data
      } catch (error) {
        throw new Error('Request failed')
      } finally {
        setLoading(false)
      }
    },
    []
  )

  return (
    <PaymentContext.Provider
      value={{
        createPayment,
        loading,
        payment,
      }}
    >
      {children}
    </PaymentContext.Provider>
  )
}
