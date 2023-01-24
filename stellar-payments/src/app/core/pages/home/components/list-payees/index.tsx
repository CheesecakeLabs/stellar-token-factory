import React, { useEffect } from 'react'

import { usePayees } from 'services/hooks/usePayees'

import { Loading } from 'components/atoms'

import { ItemPayee } from '../item-payee'
import styles from './styles.module.scss'

export const ListPayees: React.FC = () => {
  const { getPayees, loading, payees } = usePayees()

  useEffect(() => {
    getPayees()
  }, [getPayees])

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
                <th>Phone</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {payees &&
                payees.map(item => {
                  return <ItemPayee payee={item} />
                })}
            </tbody>
          </>
        )}
      </table>
    </div>
  )
}
