import React, { useState } from 'react'

import { DeleteOutlined } from '@ant-design/icons'
import { ConfigProvider, message, Modal } from 'antd'
import { usePayment } from 'services/hooks/usePayment'

import {
  Button,
  ButtonVariant,
  Typography,
  TypographyVariant,
} from 'components/atoms'

import { AuthService } from 'app/core/auth/auth-service'

import styles from './styles.module.scss'

export const Settings: React.FC = () => {
  const { clearPayments, getLocalPayments } = usePayment()

  const [openModalDelete, setModalDelete] = useState(false)

  const hideModal = (): void => {
    setModalDelete(false)
  }

  const permissions = (): string => {
    if (AuthService.currentUser().email == 'john') {
      return 'You are allowed to complete payments via Stellar Pay yourself.'
    }
    return 'You need an extra approval to make payments via Stellar Pay'
  }

  const deletePayments = (): void => {
    clearPayments()
    getLocalPayments(AuthService.currentUser().email)
    hideModal()
    message.success('Cleared payment history')
  }

  return (
    <>
      <ConfigProvider
        theme={{
          token: {
            colorPrimary: '#d26666',
          },
        }}
      >
        <Modal
          title="Modal"
          open={openModalDelete}
          onOk={deletePayments}
          onCancel={hideModal}
          okText="Yes, delete"
          cancelText="Cancel"
        >
          <p>
            Are you sure you want to delete the payment history created by you?
          </p>
        </Modal>
      </ConfigProvider>

      <div className={styles.container}>
        <div className={styles.containerSetting}>
          <div className={styles.column}>
            <Typography
              variant={TypographyVariant.label}
              text={'Permissions'}
              className={styles.title}
            />
            <Typography
              variant={TypographyVariant.label}
              text={permissions()}
              className={styles.description}
            />
          </div>
        </div>
        <div className={styles.containerSetting}>
          <div className={styles.column}>
            <Typography
              variant={TypographyVariant.label}
              text={'Clear payments history'}
              className={styles.title}
            />
            <Typography
              variant={TypographyVariant.label}
              text={
                'This action will delete the payment history created by you.'
              }
              className={styles.description}
            />
          </div>
          <Button
            variant={ButtonVariant.delete}
            label={'Delete payments'}
            icon={<DeleteOutlined />}
            onClick={(): void => {
              setModalDelete(true)
            }}
          />
        </div>
      </div>
    </>
  )
}
