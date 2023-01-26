import { useContext } from 'react'

import { PaymentContext } from './context'

export function usePayment(): Hooks.UsePaymentTypes.IPaymentContext {
  const context = useContext(PaymentContext)

  if (!context) {
    throw new Error('usePayment must be used within an PaymentProvider')
  }

  return context
}
