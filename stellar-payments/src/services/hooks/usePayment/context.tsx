import { createContext, useCallback, useState } from 'react'

import { LOCAL_STORAGE_PREFIX } from 'services/utils/constants'

import { http } from 'interfaces/http'

export const PaymentContext = createContext(
  {} as Hooks.UsePaymentTypes.IPaymentContext
)

export const PaymentProvider: React.FC = ({ children }) => {
  const PENDING_SIGNERS = `${LOCAL_STORAGE_PREFIX}/pending_signers`

  const [payment, setPayment] = useState<Hooks.UsePaymentTypes.IPayment>()
  const [submit, setSubmit] = useState<Hooks.UsePaymentTypes.ISubmit>()
  const [pendingSigners, setPendingSigners] =
    useState<Hooks.UsePaymentTypes.IPendingSigner[]>()
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

  const makeSubmit = useCallback(
    async (
      params: Hooks.UsePaymentTypes.ISubmitParams
    ): Promise<Hooks.UsePaymentTypes.ISubmit | undefined> => {
      setLoading(true)
      try {
        const response = await http.post(`/api/payments/submit`, params)
        setSubmit(response.data)
        return response.data
      } catch (error) {
        throw new Error('Request failed')
      } finally {
        setLoading(false)
      }
    },
    []
  )

  const addUserToPendingSigners = (
    data: Hooks.UsePaymentTypes.IPendingSigner
  ): boolean => {
    try {
      const list = localStorage.getItem(PENDING_SIGNERS)
      const result = list ? JSON.parse(list) : []
      result.push(data)

      localStorage.setItem(PENDING_SIGNERS, JSON.stringify(result))
      return true
    } catch (error) {
      return false
    }
  }

  const getPendingSigners = (
    user: string
  ): Hooks.UsePaymentTypes.IPendingSigner[] => {
    const list = localStorage.getItem(PENDING_SIGNERS)
    const result = list ? JSON.parse(list) : []
    const filtered = result.filter(
      (item: Hooks.UsePaymentTypes.IPendingSigner) => item.user_id == user
    )
    setPendingSigners(filtered)
    return filtered
  }

  return (
    <PaymentContext.Provider
      value={{
        createPayment,
        loading,
        payment,
        submit,
        makeSubmit,
        addUserToPendingSigners,
        getPendingSigners,
        pendingSigners,
      }}
    >
      {children}
    </PaymentContext.Provider>
  )
}
