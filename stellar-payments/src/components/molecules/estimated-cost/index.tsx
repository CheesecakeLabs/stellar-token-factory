import { useTranslation } from 'react-i18next'

import { InfoCircleFilled } from '@ant-design/icons'
import { toEur } from 'services/utils/utils'

import {
  Row,
  RowContent,
  Typography,
  TypographyVariant,
} from 'components/atoms'
import { BlockchainIcon } from 'components/icons'

import styles from './styles.module.scss'

interface IEstimatedCost {
  amount: number
  payment: Hooks.UsePaymentTypes.IPayment | undefined
}

export const EstimatedCost: React.FC<IEstimatedCost> = ({ payment }) => {
  const { t } = useTranslation()

  return (
    <div className={styles.container}>
      <div className={styles.containerFormPayment}>
        <div className={styles.formPayment}>
          <div className={styles.containerTitle}>
            <BlockchainIcon width={48} height={48} />
            <Typography
              variant={TypographyVariant.p}
              text={t('stellar_pay')}
              className={styles.title}
            />
          </div>
          <>
            <Row justifyContent={RowContent.spaceBetween}>
              <Typography
                variant={TypographyVariant.label}
                text={t('fees')}
                className={styles.label}
              />
              <Typography
                variant={TypographyVariant.p}
                text={'< $ 0.01'}
                className={styles.value}
              />
            </Row>
            <Row justifyContent={RowContent.spaceBetween}>
              <Typography
                variant={TypographyVariant.label}
                text={t('eta')}
                className={styles.label}
              />
              <Typography
                variant={TypographyVariant.p}
                text={'< 10s'}
                className={styles.value}
              />
            </Row>
            <Row justifyContent={RowContent.spaceBetween}>
              <Typography
                variant={TypographyVariant.label}
                text={t('exchange')}
                className={styles.label}
              />
              <Typography
                variant={TypographyVariant.p}
                text={'1.10 USD/EUR'}
                className={styles.value}
              />
            </Row>
            <div className={styles.divider} />
            <Row justifyContent={RowContent.spaceBetween}>
              <Typography
                variant={TypographyVariant.label}
                text={t('final_cost')}
                className={styles.label}
              />
              <Typography
                variant={TypographyVariant.p}
                text={toEur(payment ? payment.final_cost : 0)}
                className={styles.value}
              />
            </Row>
            <div className={styles.requestSignature}>
              <InfoCircleFilled style={{ fontSize: '16px' }} />
              <Typography
                variant={TypographyVariant.label}
                text={`1/2 ${t('approvals_required')}}`}
                className={styles.message}
              />
            </div>
          </>
        </div>
      </div>
    </div>
  )
}
