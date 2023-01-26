import { useContext } from 'react'

import { PayeesContext } from './context'

export function usePayees(): Hooks.UsePayeesTypes.IPayeesContext {
  const context = useContext(PayeesContext)

  if (!context) {
    throw new Error('usePayees must be used within an PayeesProvider')
  }

  return context
}
