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
  pendingPayments: Hooks.UsePaymentTypes.IPendingSigner[] | undefined
  getData(): void
}

export const ModalPending: React.FC<IModalStellarPayProps> = ({
  isOpen,
  setOpenModal,
  pendingPayments,
  getData,
}) => {
  const { loading, makeSubmit, submit, removePendingSigners, setSubmit } =
    usePayment()

  const closeModal = (): void => {
    setOpenModal(false)
    setSubmit(undefined)
    getData()
  }

  const confirmPayment = async (): Promise<void> => {
    if (!pendingPayments || !pendingPayments[0]) return

    const data = {
      envelope_xdr: pendingPayments[0].envelope_xdr,
      sign: pendingPayments[0].sign,
      user_id: AuthService.currentUser().email,
    }

    await makeSubmit(data).then(result => {
      if (result) {
        removePendingSigners(pendingPayments[0])
        return
      }
      message.error('An error occurred. Please try again...')
    })
  }

  return (
    <Modal isOpen={isOpen} handleClose={closeModal} title="Pending payment">
      {!submit ? (
        <>
          {pendingPayments && pendingPayments[0] && (
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
                  eur_price: pendingPayments[0].eur_price,
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
      ) : (
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
      )}
    </Modal>
  )
}
