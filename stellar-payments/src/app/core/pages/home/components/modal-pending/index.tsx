import React, { Dispatch, SetStateAction } from 'react'

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
  payment: Hooks.UsePaymentTypes.IPaymentData
}

export const ModalPending: React.FC<IModalStellarPayProps> = ({
  isOpen,
  setOpenModal,
  payment,
}) => {
  const { loading, makeSubmit, submit, updatePayment } = usePayment()

  const closeModal = (): void => {
    setOpenModal(false)
    if (submit) window.location.reload()
  }

  const confirmPayment = async (): Promise<void> => {
    if (!payment) return

    try {
      const data = {
        envelope_xdr: payment.envelope_xdr,
        sign: payment.sign,
        user_id: AuthService.currentUser().email,
      }

      await makeSubmit(data).then(result => {
        payment.transactionLink = result?.transaction_link
        updatePayment(payment)
        return
      })
    } catch (error) {
      message.error('An error occurred. Please try again...')
    }
  }

  return (
    <Modal isOpen={isOpen} handleClose={closeModal} title="Pending payment">
      {submit ? (
        payment && (
          <StatusTransaction
            amount={payment.amount}
            submit={submit}
            formPayment={TypePayment.stellar}
            payee={{
              name: payment.payee,
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
          {payment && (
            <div className={styles.container}>
              <div className={styles.containerCosts}>
                <Row justifyContent={RowContent.spaceBetween}>
                  <Typography
                    variant={TypographyVariant.label}
                    text={'Payment amount'}
                    className={styles.label}
                  />
                  <Typography
                    variant={TypographyVariant.p}
                    text={toUsd(payment.amount)}
                    className={styles.value}
                  />
                </Row>
              </div>
              <EstimatedCost
                amount={payment.amount ?? 0}
                payment={{
                  envelope_xdr: payment.envelope_xdr,
                  final_cost: payment.final_cost,
                  required_signatures: [],
                  usd_price: payment.usd_price,
                }}
              />
              <Button
                variant={ButtonVariant.tertiary}
                label={'Approve payment'}
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
