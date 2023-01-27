import React, { Dispatch, SetStateAction, useState } from 'react'

import { LeftOutlined } from '@ant-design/icons'
import { ConfigProvider, message, Steps } from 'antd'
import { usePayment } from 'services/hooks/usePayment'
import { formatValueToNumber } from 'services/utils/utils'

import { Button, ButtonVariant, Modal } from 'components/atoms'
import { TypePayment } from 'components/enums'
import { Amount, Payment, StatusTransaction } from 'components/molecules'

import { AuthService } from 'app/core/auth/auth-service'

import styles from './styles.module.scss'

interface IModalStellarPayProps {
  isOpen: boolean
  setOpenModal: Dispatch<SetStateAction<boolean>>
  payee: Hooks.UsePayeesTypes.IPayee
}

export const ModalStellarPay: React.FC<IModalStellarPayProps> = ({
  isOpen,
  setOpenModal,
  payee,
}) => {
  const [current, setCurrent] = useState(0)
  const [amount, setAmount] = useState<string>()
  const [formPayment, setFormPayment] = useState<TypePayment>()
  const {
    createPayment,
    loading,
    payment,
    makeSubmit,
    submit,
    addUserToPendingSigners,
  } = usePayment()

  const next = (): void => {
    setCurrent(current + 1)
  }

  const prev = (): void => {
    setCurrent(current - 1)
  }

  function handleChange(value: string): void {
    setAmount(value)
  }

  const closeModal = (): void => {
    setCurrent(0)
    setAmount(undefined)
    setFormPayment(undefined)
    setOpenModal(false)
  }

  const sendAmount = async (): Promise<void> => {
    const data = {
      destination_public_key: payee.stellar_wallet,
      receive_amount: formatValueToNumber(amount),
      user_id: AuthService.currentUser().email,
    }
    await createPayment(data).then(payment => {
      if (payment != null) {
        return next()
      }
      message.error('An error occurred. Please try again...')
    })
  }

  const confirmPayment = async (): Promise<void> => {
    if (!payment) return

    const data = {
      envelope_xdr: payment.envelope_xdr,
      sign: payment.required_signatures.length ?? 0,
      user_id: AuthService.currentUser().email,
    }

    await makeSubmit(data).then(result => {
      if (result != null) {
        return next()
      }
      message.error('An error occurred. Please try again...')
    })
  }

  const addToPendingSigner = async (): Promise<void> => {
    if (!payment) return

    const data = {
      envelope_xdr: payment.envelope_xdr,
      final_cost: payment.final_cost,
      eur_price: payment.eur_price,
      amount: formatValueToNumber(amount),
      sign: 1,
      user_id: payment.required_signatures[0],
      date: Date.now(),
    }

    if (addUserToPendingSigners(data)) {
      return next()
    }
    message.error('An error occurred. Please try again...')
  }

  const noRequestSignature = (): boolean => {
    return (
      !payment?.required_signatures ||
      formPayment == TypePayment.wire ||
      formPayment == undefined
    )
  }

  const steps = [
    {
      title: 'Order',
      content: (
        <Amount amount={amount} onChangeText={handleChange} payee={payee} />
      ),
      label: 'Create payment',
      action: sendAmount,
      isDisabled: !amount,
    },
    {
      title: 'Payment Quote',
      content: (
        <Payment
          amount={formatValueToNumber(amount)}
          payment={payment}
          formPayment={formPayment}
          setFormPayment={setFormPayment}
        />
      ),
      label: noRequestSignature() ? 'Confirm payment' : 'Approve payment',
      action: noRequestSignature() ? confirmPayment : addToPendingSigner,
    },
    {
      title: 'Confirmation',
      content: (
        <StatusTransaction
          amount={formatValueToNumber(amount)}
          submit={submit}
          formPayment={formPayment}
          payee={payee}
          isMultiSignatures={!noRequestSignature()}
        />
      ),
      label: 'Next',
      action: closeModal,
    },
  ]

  const items = steps.map(item => ({ key: item.title, title: item.title }))

  return (
    <Modal isOpen={isOpen} handleClose={closeModal} title="Payment">
      <div className={styles.container}>
        <div>
          <ConfigProvider
            theme={{
              token: {
                colorPrimary: '#34495e',
              },
            }}
          >
            <Steps
              current={current}
              items={items}
              className={styles.steps}
              size={'small'}
            />
          </ConfigProvider>
          <div className={styles.content}>{steps[current].content}</div>
        </div>
        <div className={styles.containerControllers}>
          {current > 0 && current < steps.length - 1 ? (
            <Button
              variant={ButtonVariant.icon}
              onClick={(): void => prev()}
              label=""
              icon={<LeftOutlined />}
            />
          ) : (
            <div />
          )}
          {current < steps.length - 1 && (
            <Button
              variant={ButtonVariant.tertiary}
              onClick={steps[current].action ?? undefined}
              label={steps[current].label}
              isLoading={loading}
              isDisabled={steps[current].isDisabled}
            />
          )}
        </div>
      </div>
    </Modal>
  )
}
