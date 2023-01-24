import React from 'react'

import { PayeesProvider } from './usePayees/context'

export const AppProvider: React.FC = ({ children }) => {
  return <PayeesProvider>{children}</PayeesProvider>
}
