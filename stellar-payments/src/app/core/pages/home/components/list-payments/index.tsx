import React from 'react'

import { Loading } from 'components/atoms'

import styles from './styles.module.scss'

interface IListPaymentsProps {
  loading: boolean
  payments: Hooks.UsePaymentTypes.IPaymentData[] | undefined
}

export const ListPayments: React.FC<IListPaymentsProps> = ({
  loading,
  payments,
}) => {
  return (
    <div className={styles.container}>
      <table>
        {loading ? (
          <Loading />
        ) : (
          <>
            <thead>
              <tr>
                <th>Payee</th>
                <th>Amount</th>
                <th>Creation date</th>
                <th>Expiration date</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {payments &&
                payments.map(item => {
                  return <div>oi</div>
                })}
            </tbody>
          </>
        )}
      </table>
    </div>
  )
}
