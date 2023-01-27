import { CheckCircleFilled, FieldTimeOutlined, LinkOutlined } from '@ant-design/icons'
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
  payee: Hooks.UsePayeesTypes.IPayee
  isMultiSignatures: boolean
}

export const StatusTransaction: React.FC<IStatusTransaction> = ({
  amount,
  submit,
  formPayment,
  payee,
  isMultiSignatures,
}) => {
  return (
    <div className={styles.container}>
      {isMultiSignatures ? (
        <FieldTimeOutlined style={{ fontSize: '2rem', color: '#303549' }} />
      ) : (
        <CheckCircleFilled style={{ fontSize: '2rem', color: '#16a085' }} />
      )}
      <Typography
        variant={TypographyVariant.label}
        text={isMultiSignatures ? 'Pending' : 'Success!'}
        className={styles.statusMessage}
      />
      <Typography
        variant={TypographyVariant.label}
        text={
          isMultiSignatures
            ? 'Waiting for signatures (1/2)'
            : `You made a payment of ${toUsd(amount)} to ${payee.name} using ${
                formPayment == TypePayment.stellar
                  ? 'Stellar Pay'
                  : 'Wire Transfer'
              }`
        }
        className={styles.descriptionMessage}
      />
      <Button
        variant={ButtonVariant.primary}
        label={'Open in Stellar Expert'}
        onClick={(): Window | null =>
          window.open(submit?.transaction_link, '_blank')
        }
        icon={<LinkOutlined />}
      />
    </div>
  )
}
