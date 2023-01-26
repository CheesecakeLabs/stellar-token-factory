import React, { Dispatch, SetStateAction, useState } from 'react'

import { LeftOutlined } from '@ant-design/icons'
import { ConfigProvider, message, Steps } from 'antd'
import { MessageType } from 'antd/es/message/interface'
import { usePayment } from 'services/hooks/usePayment'
import { formatValueToNumber } from 'services/utils/utils'

import { Button, ButtonVariant, Modal } from 'components/atoms'
import { Amount, EstimatedCost, StatusTransaction } from 'components/molecules'

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
  const { createPayment, loading, payment } = usePayment()

  const next = (): void => {
    setCurrent(current + 1)
  }

  const prev = (): void => {
    setCurrent(current - 1)
  }

  function handleChange(value: string): void {
    setAmount(value)
  }

  const sendAmount = async (): Promise<void> => {
    const data = {
      destination_public_key: payee.stellar_wallet,
      receive_amount: formatValueToNumber(amount),
    }
    await createPayment(data).then(payment => {
      if (payment != null) {
        return next()
      }
      message.error('An error occurred. Please try again...')
    })
  }

  const steps = [
    {
      title: 'Amount',
      content: (
        <Amount amount={amount} onChangeText={handleChange} payee={payee} />
      ),
      label: 'Create payment',
      action: sendAmount,
      isDisabled: !amount,
    },
    {
      title: 'Costs',
      content: (
        <EstimatedCost amount={formatValueToNumber(amount)} payment={payment} />
      ),
      label: 'Confirm payment',
    },
    {
      title: 'Finished',
      content: <StatusTransaction />,
      label: 'Next',
    },
  ]

  const items = steps.map(item => ({ key: item.title, title: item.title }))

  return (
    <Modal isOpen={isOpen} handleClose={(): void => setOpenModal(false)}>
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
          {current > 0 ? (
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
          {current === steps.length - 1 && (
            <Button
              variant={ButtonVariant.tertiary}
              onClick={(): MessageType =>
                message.success('Processing complete!')
              }
              label="Done"
            />
          )}
        </div>
      </div>
    </Modal>
  )
}
