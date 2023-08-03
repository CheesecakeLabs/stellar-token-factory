import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'

import { DollarOutlined, WarningOutlined } from '@ant-design/icons'

import {
  Button,
  ButtonVariant,
  Row,
  Typography,
  TypographyVariant,
} from 'components/atoms'
import { ArrowDown, ArrowUp } from 'components/icons'

import { ModalPending } from '../modal-pending'
import { ModalStellarPay } from '../modal-stellar-pay'
import styles from './styles.module.scss'

interface IItemPayeeProps {
  payee: Hooks.UsePayeesTypes.IPayee
}

export const ItemPayee: React.FC<IItemPayeeProps> = ({ payee }) => {
  const [isExpanded, setExpanded] = useState(false)
  const [isOpenStellarPay, setModalStellarPay] = useState(false)
  const [isOpenPending, setModalPending] = useState(false)
  const { t } = useTranslation()

  const openModalStellar = (
    event: React.MouseEvent<HTMLButtonElement>
  ): void => {
    event.stopPropagation()
    setModalStellarPay(true)
  }

  const openModalPending = (
    event: React.MouseEvent<HTMLButtonElement>
  ): void => {
    event.stopPropagation()
    setModalPending(true)
  }

  const isPending = (): boolean => {
    if (!payee || !payee.payments) return false
    return payee.payments.length > 0
  }

  return (
    <>
      <ModalStellarPay
        isOpen={isOpenStellarPay}
        setOpenModal={setModalStellarPay}
        payee={payee}
      />
      <ModalPending
        isOpen={isOpenPending}
        setOpenModal={setModalPending}
        pendingPayments={payee.payments}
      />
      <tr onClick={(): void => setExpanded(!isExpanded)}>
        <td className={styles.tdDetails}>
          {isExpanded ? (
            <ArrowUp width={12} height={12} className={styles.arrow} />
          ) : (
            <ArrowDown width={12} height={12} className={styles.arrow} />
          )}
        </td>
        <td>{payee.name}</td>
        <td className={styles.tdPhone}>{payee.phone}</td>
        <td className={styles.alignEnd}>
          <Row>
            <Button
              variant={
                isPending() ? ButtonVariant.warning : ButtonVariant.primary
              }
              label={
                isPending() ? t('pending_approval') : t('create_payment_order')
              }
              icon={isPending() ? <WarningOutlined /> : <DollarOutlined />}
              onClick={isPending() ? openModalPending : openModalStellar}
            />
          </Row>
        </td>
      </tr>
      {isExpanded && (
        <tr className={styles.expandable}>
          <td colSpan={6}>
            <div className={styles.containerDatails}>
              <Typography
                variant={TypographyVariant.label}
                text={t('address')}
                className={styles.label}
              />
              <Typography
                variant={TypographyVariant.p}
                text={payee.address}
                className={styles.value}
              />
              <div className={styles.detailPhone}>
                <Typography
                  variant={TypographyVariant.label}
                  text={t('phone')}
                  className={styles.label}
                />
                <Typography
                  variant={TypographyVariant.p}
                  text={payee.phone}
                  className={styles.value}
                />
              </div>
              <Typography
                variant={TypographyVariant.label}
                text={t('bank_account')}
                className={styles.label}
              />
              <Typography
                variant={TypographyVariant.p}
                text={payee.bank_account}
                className={styles.value}
              />
              <Typography
                variant={TypographyVariant.label}
                text={t('stellar_wallet')}
                className={styles.label}
              />
              <Typography
                variant={TypographyVariant.p}
                text={payee.stellar_wallet}
                className={styles.value}
              />
            </div>
          </td>
        </tr>
      )}
    </>
  )
}
