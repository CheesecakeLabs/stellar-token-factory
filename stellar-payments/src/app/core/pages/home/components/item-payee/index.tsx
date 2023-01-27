import React, { useCallback, useEffect, useState } from 'react'

import { DollarOutlined, WarningOutlined } from '@ant-design/icons'

import {
  Button,
  ButtonVariant,
  Row,
  Typography,
  TypographyVariant,
} from 'components/atoms'
import { ArrowDown, ArrowUp } from 'components/icons'

import { AuthService } from 'app/core/auth/auth-service'

import { ModalPending } from '../modal-pending'
import { ModalStellarPay } from '../modal-stellar-pay'
import styles from './styles.module.scss'

interface IItemPayeeProps {
  payee: Hooks.UsePayeesTypes.IPayee
  pendingSigners: Hooks.UsePaymentTypes.IPendingSigner[] | undefined
  getData(): void
}

export const ItemPayee: React.FC<IItemPayeeProps> = ({
  payee,
  pendingSigners,
  getData,
}) => {
  const [isExpanded, setExpanded] = useState(false)
  const [isOpenStellarPay, setModalStellarPay] = useState(false)
  const [isOpenPending, setModalPending] = useState(false)
  const [pendingPayments, setPendingPayments] = useState<
    Hooks.UsePaymentTypes.IPendingSigner[]
  >([])

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

  const getPendingPayments =
    useCallback((): Hooks.UsePaymentTypes.IPendingSigner[] => {
      const filtered = !pendingSigners
        ? []
        : pendingSigners.filter(
            item =>
              item.payee == payee.name &&
              item.user_id == AuthService.currentUser().email
          )
      setPendingPayments(filtered)
      return filtered
    }, [payee.name, pendingSigners])

  const isPending = (): boolean => {
    return pendingPayments.length > 0
  }

  useEffect(() => {
    getPendingPayments()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

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
        pendingPayments={pendingPayments}
        getData={getData}
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
              label={isPending() ? 'Pending payment' : 'Create payment order'}
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
                text={'Address'}
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
                  text={'Phone'}
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
                text={'Bank account'}
                className={styles.label}
              />
              <Typography
                variant={TypographyVariant.p}
                text={payee.bank_account}
                className={styles.value}
              />
              <Typography
                variant={TypographyVariant.label}
                text={'Stellar wallet'}
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
