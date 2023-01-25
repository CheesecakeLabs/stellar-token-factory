import React, { Dispatch, SetStateAction, useState } from 'react'

import { ConfigProvider, message, Steps } from 'antd'
import { MessageType } from 'antd/es/message/interface'

import { Button, ButtonVariant, Modal } from 'components/atoms'
import { Amount, EstimatedCost, StatusTransaction } from 'components/molecules'

import styles from './styles.module.scss'

interface IModalStellarPayProps {
  isOpen: boolean
  setOpenModal: Dispatch<SetStateAction<boolean>>
  payee: Hooks.UsePayeesTypes.IPayee
}

export const ModalStellarPay: React.FC<IModalStellarPayProps> = (
  props: IModalStellarPayProps
) => {
  const [current, setCurrent] = useState(0)

  const steps = [
    {
      title: 'Amount',
      content: <Amount />,
      label: 'Next',
    },
    {
      title: 'Estimated Cost',
      content: <EstimatedCost />,
      label: 'Send transaction',
    },
    {
      title: 'Finished',
      content: <StatusTransaction />,
      label: 'Next',
    },
  ]

  const items = steps.map(item => ({ key: item.title, title: item.title }))

  const next = (): void => {
    setCurrent(current + 1)
  }

  const prev = (): void => {
    setCurrent(current - 1)
  }

  return (
    <Modal
      isOpen={props.isOpen}
      handleClose={(): void => props.setOpenModal(false)}
    >
      <div className={styles.container}>
        <div>
          <ConfigProvider
            theme={{
              token: {
                colorPrimary: '#16a085',
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
              variant={ButtonVariant.tertiary}
              onClick={(): void => prev()}
              label="Previous"
            />
          ) : (
            <div />
          )}
          {current < steps.length - 1 && (
            <Button
              variant={ButtonVariant.tertiary}
              onClick={(): void => next()}
              label={steps[current].label}
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
