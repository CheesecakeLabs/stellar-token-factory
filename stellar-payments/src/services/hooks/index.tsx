import React from 'react'

import { AccountProvider } from './useAccount/context'
import { PayeesProvider } from './usePayees/context'
import { PaymentProvider } from './usePayment/context'

export const AppProvider: React.FC = ({ children }) => {
  return (
    <AccountProvider>
      <PaymentProvider>
        <PayeesProvider>{children}</PayeesProvider>
      </PaymentProvider>
    </AccountProvider>
  )
}
