import React, { Dispatch, SetStateAction, useState } from 'react'

import { message, Steps } from 'antd'
import { MessageType } from 'antd/es/message/interface'

import { Button, ButtonVariant, Modal } from 'components/atoms'
import { Amount } from 'components/molecules'

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
    },
    {
      title: 'Estimated Cost',
      content: 'Second-content',
    },
    {
      title: 'Finished',
      content: 'Last-content',
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
      <Steps
        current={current}
        items={items}
        className={styles.steps}
        size={'small'}
      />
      <div>{steps[current].content}</div>
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
            label="Next"
          />
        )}
        {current === steps.length - 1 && (
          <Button
            variant={ButtonVariant.tertiary}
            onClick={(): MessageType => message.success('Processing complete!')}
            label="Done"
          />
        )}
      </div>
    </Modal>
  )
}
