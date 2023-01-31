import React, { useState } from 'react'

import {
  CheckCircleOutlined,
  FieldTimeOutlined,
  LinkOutlined,
  WarningOutlined,
} from '@ant-design/icons'
import { formatDate, toEur, toUsd } from 'services/utils/utils'

import { Button, ButtonVariant, Row } from 'components/atoms'
import { StatusPayment, TypePayment } from 'components/enums'

import { AuthService } from 'app/core/auth/auth-service'

import { ModalPending } from '../modal-pending'
import styles from './styles.module.scss'

interface IItemPaymentProps {
  payment: Hooks.UsePaymentTypes.IPaymentData
}

export const ItemPayment: React.FC<IItemPaymentProps> = ({ payment }) => {
  const [isOpenModal, setModal] = useState(false)

  const openModal = (event: React.MouseEvent<HTMLButtonElement>): void => {
    event.stopPropagation()
    setModal(true)
  }

  const openStellarExpert = (): void => {
    window.open(payment.transactionLink, '_blank')
  }

  const isConcluded = (): boolean => {
    return payment.status == StatusPayment.concluded
  }

  const showButton = (): boolean => {
    return (
      payment.typePayment == TypePayment.stellar &&
      !(
        payment.status == StatusPayment.waiting &&
        payment.user_id != AuthService.currentUser().email
      )
    )
  }
  return (
    <>
      <ModalPending
        isOpen={isOpenModal}
        setOpenModal={setModal}
        payment={payment}
      />
      <tr>
        <td>
          {payment.status == StatusPayment.concluded ? (
            <CheckCircleOutlined
              style={{ fontSize: '1rem', color: '#16a085' }}
            />
          ) : (
            <FieldTimeOutlined style={{ fontSize: '1rem', color: '#a2a2a2' }} />
          )}
        </td>
        <td>{payment.payee}</td>
        <td>{toUsd(payment.amount)}</td>
        <td>
          {toEur(
            payment.typePayment == TypePayment.stellar
              ? payment.final_cost
              : payment.final_cost + 20
          )}
        </td>
        <td>{payment.typePayment}</td>
        <td>{formatDate(payment.createdAt)}</td>
        <td className={styles.alignEnd}>
          {showButton() && (
            <Row>
              <Button
                variant={
                  isConcluded() ? ButtonVariant.primary : ButtonVariant.warning
                }
                label={
                  isConcluded() ? 'Open in Stellar Expert' : 'Approval payment'
                }
                icon={
                  payment.status == StatusPayment.concluded ? (
                    <LinkOutlined />
                  ) : (
                    <WarningOutlined />
                  )
                }
                onClick={
                  payment.status == StatusPayment.concluded
                    ? openStellarExpert
                    : openModal
                }
              />
            </Row>
          )}
        </td>
      </tr>
    </>
  )
}
