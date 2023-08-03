import React, { Dispatch, SetStateAction } from 'react'
import { useTranslation } from 'react-i18next'

import { message } from 'antd'
import { usePayment } from 'services/hooks/usePayment'
import { toUsd } from 'services/utils/utils'

import {
  Button,
  ButtonVariant,
  Modal,
  Row,
  RowContent,
  Typography,
  TypographyVariant,
} from 'components/atoms'
import { TypePayment } from 'components/enums'
import { EstimatedCost, StatusTransaction } from 'components/molecules'

import { AuthService } from 'app/core/auth/auth-service'

import styles from './styles.module.scss'

interface IModalStellarPayProps {
  isOpen: boolean
  setOpenModal: Dispatch<SetStateAction<boolean>>
  pendingPayments: Hooks.UsePaymentTypes.IPendingSigner[] | undefined
}

export const ModalPending: React.FC<IModalStellarPayProps> = ({
  isOpen,
  setOpenModal,
  pendingPayments,
}) => {
  const { loading, makeSubmit, submit, removePendingSigners } = usePayment()
  const { t } = useTranslation()

  const closeModal = (): void => {
    setOpenModal(false)
    if (submit) window.location.reload()
  }

  const confirmPayment = async (): Promise<void> => {
    if (!pendingPayments || !pendingPayments[0]) return

    try {
      const data = {
        envelope_xdr: pendingPayments[0].envelope_xdr,
        sign: pendingPayments[0].sign,
        user_id: AuthService.currentUser().email,
      }

      await makeSubmit(data).then(() => {
        removePendingSigners(pendingPayments[0])
        return
      })
    } catch (error) {
      message.error(t('error_occurred'))
    }
  }

  return (
    <Modal
      isOpen={isOpen}
      handleClose={closeModal}
      title={t('pending_payment')}
    >
      {submit ? (
        pendingPayments &&
        pendingPayments[0] && (
          <StatusTransaction
            amount={pendingPayments[0].amount}
            submit={submit}
            formPayment={TypePayment.stellar}
            payee={{
              name: pendingPayments[0].payee,
              address: '',
              phone: '',
              bank_account: '',
              stellar_wallet: '',
            }}
            isMultiSignatures={false}
          />
        )
      ) : (
        <>
          {pendingPayments && pendingPayments[0] && (
            <div className={styles.container}>
              <div className={styles.containerCosts}>
                <Row justifyContent={RowContent.spaceBetween}>
                  <Typography
                    variant={TypographyVariant.label}
                    text={t('payment_amount')}
                    className={styles.label}
                  />
                  <Typography
                    variant={TypographyVariant.p}
                    text={toUsd(pendingPayments[0].amount)}
                    className={styles.value}
                  />
                </Row>
              </div>
              <EstimatedCost
                amount={pendingPayments[0].amount ?? 0}
                payment={{
                  envelope_xdr: pendingPayments[0].envelope_xdr,
                  final_cost: pendingPayments[0].final_cost,
                  required_signatures: [],
                  usd_price: pendingPayments[0].usd_price,
                }}
              />
              <Button
                variant={ButtonVariant.tertiary}
                label={t('approve_payment')}
                isLoading={loading}
                onClick={confirmPayment}
              />
            </div>
          )}
        </>
      )}
    </Modal>
  )
}
