import { useTranslation } from 'react-i18next'

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
  const { t } = useTranslation()

  return (
    <div className={styles.container}>
      {isMultiSignatures ? (
        <FieldTimeOutlined style={{ fontSize: '4rem', color: '#303549' }} />
      ) : (
        <CheckCircleFilled style={{ fontSize: '4rem', color: '#16a085' }} />
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
            ? `${t('waiting_approvals')} (1/2)`
            : `${t('you_made_payment')} ${toUsd(amount)} ${t('to')} ${
                payee.name
              } ${t('using')} ${
                formPayment == TypePayment.stellar
                  ? t('stellar_pay')
                  : t('wire_transfer')
              }`
        }
        className={styles.descriptionMessage}
      />
      {!isMultiSignatures && formPayment == TypePayment.stellar && (
        <div className={styles.openLink}>
          <Button
            variant={ButtonVariant.primary}
            label={t('open_stellar_expert')}
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
