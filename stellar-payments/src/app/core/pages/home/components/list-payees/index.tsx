import React, { useEffect } from 'react'

import { usePayment } from 'services/hooks/usePayment'

import { Loading } from 'components/atoms'

import { AuthService } from 'app/core/auth/auth-service'

import { ItemPayee } from '../item-payee'
import styles from './styles.module.scss'

interface IListPayeesProps {
  loading: boolean
  payees: Hooks.UsePayeesTypes.IPayee[] | undefined
}

export const ListPayees: React.FC<IListPayeesProps> = ({ loading, payees }) => {
  const { getPendingSigners, pendingSigners } = usePayment()

  useEffect(() => {
    getPendingSigners(AuthService.currentUser().email)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <div className={styles.container}>
      <table>
        {loading ? (
          <Loading />
        ) : (
          <>
            <thead>
              <tr>
                <th></th>
                <th>Company name</th>
                <th className={styles.thPhone}>Phone</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {payees &&
                payees.map(item => {
                  return (
                    <ItemPayee payee={item} pendingSigners={pendingSigners} />
                  )
                })}
            </tbody>
          </>
        )}
      </table>
    </div>
  )
}
