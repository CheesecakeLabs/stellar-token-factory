import { FunctionComponent } from 'react'
import { Button, Modal } from '@stellar/design-system'
import styles from './styles.module.scss'

export interface IConfirmModalProps {
  isModalVisible: boolean
  closeModal: () => void
  submit: () => void
  message: string
}

const ConfirmModal: FunctionComponent<IConfirmModalProps> = props => {
  return (
    <Modal onClose={props.closeModal} visible={props.isModalVisible}>
      <p>{props.message}</p>
      <div className={styles.contentButtons}>
        <Button variant={Button.variant.tertiary} onClick={props.closeModal}>
          Cancel
        </Button>
        <Button
          variant={Button.variant.primary}
          onClick={(): void => props.submit()}
        >
          Confirm
        </Button>
      </div>
    </Modal>
  )
}

export { ConfirmModal }
