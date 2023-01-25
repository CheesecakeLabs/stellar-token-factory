import React from 'react'

import { AccountProvider } from './useAccount/context'
import { PayeesProvider } from './usePayees/context'

export const AppProvider: React.FC = ({ children }) => {
  return (
    <AccountProvider>
      <PayeesProvider>{children}</PayeesProvider>
    </AccountProvider>
  )
}
