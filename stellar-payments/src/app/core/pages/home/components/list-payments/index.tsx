import React from 'react'

import { PlusCircleOutlined } from '@ant-design/icons'

import { Button, ButtonVariant, Loading, Row } from 'components/atoms'

import { ItemPayment } from '../item-payment'
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
                <th></th>
                <th>Payee</th>
                <th>Amount</th>
                <th>Final Cost</th>
                <th>Type</th>
                <th>Creation date</th>
                <th className={styles.thAddPayment}>
                  <Row>
                    <Button
                      variant={ButtonVariant.add}
                      label={'Create new payment'}
                      icon={<PlusCircleOutlined />}
                    />
                  </Row>
                </th>
              </tr>
            </thead>
            <tbody>
              {payments &&
                payments.map(item => {
                  return <ItemPayment payment={item} key={item.createdAt} />
                })} 
            </tbody>
          </>
        )}
      </table>
    </div>
  )
}
