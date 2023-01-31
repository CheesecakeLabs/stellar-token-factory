import {
  CheckCircleFilled,
  FieldTimeOutlined,
  LinkOutlined,
} from '@ant-design/icons'
import { toUsd } from 'services/utils/utils'

import {
  Button,
  ButtonVariant,
  Typography,
  TypographyVariant,
} from 'components/atoms'
import { TypePayment } from 'components/enums'

import styles from './styles.module.scss'

interface IStatusTransaction {
  amount: number
  submit: Hooks.UsePaymentTypes.ISubmit | undefined
  formPayment: TypePayment | undefined
  payee: Hooks.UsePayeesTypes.IPayee | undefined
  isMultiSignatures: boolean
}

export const StatusTransaction: React.FC<IStatusTransaction> = ({
  amount,
  submit,
  formPayment,
  payee,
  isMultiSignatures,
}) => {
  const messageDescription = (): string => {
    if (formPayment == TypePayment.wire) {
      return 'Your payment is being processed, the estimated time is 2 - 5 days'
    }
    return isMultiSignatures
      ? 'Waiting for approvals (1/2)'
      : `You made a payment of ${toUsd(amount)} to ${payee?.name} using ${
          formPayment == TypePayment.stellar ? 'Stellar Pay' : 'Wire Transfer'
        }`
  }

  const messageStatus = (): string => {
    if (formPayment == TypePayment.wire) {
      return 'Waiting for processing'
    }
    return isMultiSignatures ? 'Pending approval' : 'Success!'
  }

  return (
    <div className={styles.container}>
      {formPayment == TypePayment.wire || isMultiSignatures ? (
        <FieldTimeOutlined style={{ fontSize: '4rem', color: '#303549' }} />
      ) : (
        <CheckCircleFilled style={{ fontSize: '4rem', color: '#16a085' }} />
      )}
      <Typography
        variant={TypographyVariant.label}
        text={messageStatus()}
        className={styles.statusMessage}
      />
      <Typography
        variant={TypographyVariant.label}
        text={messageDescription()}
        className={styles.descriptionMessage}
      />
      {!isMultiSignatures && formPayment == TypePayment.stellar && (
        <div className={styles.openLink}>
          <Button
            variant={ButtonVariant.primary}
            label={'Open in Stellar Expert'}
            onClick={(): Window | null =>
              window.open(submit?.transaction_link, '_blank')
            }
            icon={<LinkOutlined />}
          />
        </div>
      )}
    </div>
  )
}
