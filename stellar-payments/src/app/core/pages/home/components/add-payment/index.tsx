import { Empty } from 'antd'

import { Button, ButtonVariant } from 'components/atoms'

import styles from './styles.module.scss'

interface IAddPaymentProps {
  onClick(): void
}

export const AddPayment: React.FC<IAddPaymentProps> = ({ onClick }) => {
  return (
    <div className={styles.container}>
      <Empty />
      <Button
        variant={ButtonVariant.tertiary}
        label={'Create new payment'}
        onClick={onClick}
      />
    </div>
  )
}
