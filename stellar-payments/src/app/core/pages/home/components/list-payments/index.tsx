import React, { useState } from 'react'

import { PlusCircleOutlined } from '@ant-design/icons'

import { Button, ButtonVariant, Loading } from 'components/atoms'

import { AddPayment } from '../add-payment'
import { ItemPayment } from '../item-payment'
import { ModalStellarPay } from '../modal-stellar-pay'
import styles from './styles.module.scss'

interface IListPaymentsProps {
  loading: boolean
  payments: Hooks.UsePaymentTypes.IPaymentData[] | undefined
  payees: Hooks.UsePayeesTypes.IPayee[] | undefined
}

export const ListPayments: React.FC<IListPaymentsProps> = ({
  loading,
  payments,
  payees,
}) => {
  const [isOpenModal, setModal] = useState(false)
  return (
    <div className={styles.container}>
      <ModalStellarPay
        isOpen={isOpenModal}
        setOpenModal={setModal}
        payees={payees}
        isSelectPayee={true}
      />
      {loading ? (
        <Loading />
      ) : (
        <table>
          <>
            <thead>
              <tr>
                <th></th>
                <th>Payee</th>
                <th>Amount</th>
                <th>Final Cost</th>
                <th>Type</th>
                <th>Creation date</th>
                <th className={styles.alignEnd}>
                  <div className={styles.containerAction}>
                    <Button
                      variant={ButtonVariant.add}
                      label={'Create new payment'}
                      icon={<PlusCircleOutlined />}
                      onClick={(): void => {
                        setModal(true)
                      }}
                    />
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              {payments && payments.length > 0 ? (
                payments.map(item => {
                  return <ItemPayment payment={item} key={item.createdAt} />
                })
              ) : (
                <tr>
                  <td colSpan={12}>
                    <AddPayment
                      onClick={(): void => {
                        setModal(true)
                      }}
                    />
                  </td>
                </tr>
              )}
            </tbody>
          </>
        </table>
      )}
    </div>
  )
}
