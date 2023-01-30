import React from 'react'

import { Loading } from 'components/atoms'

import { ItemPayee } from '../item-payee'
import styles from './styles.module.scss'

interface IListPayeesProps {
  loading: boolean
  payees: Hooks.UsePayeesTypes.IPayee[] | undefined
}

export const ListPayees: React.FC<IListPayeesProps> = ({ loading, payees }) => {
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
                    <ItemPayee payee={item} />
                  )
                })}
            </tbody>
          </>
        )}
      </table>
    </div>
  )
}
