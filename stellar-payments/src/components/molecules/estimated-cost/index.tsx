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

export const EstimatedCost: React.FC<IEstimatedCost> = ({
  payment,
}) => {
  return (
    <div className={styles.container}>
      <div className={styles.containerFormPayment}>
        <div className={styles.formPayment}>
          <div className={styles.containerTitle}>
            <BlockchainIcon width={48} height={48} />
            <Typography
              variant={TypographyVariant.p}
              text={'Stellar pay'}
              className={styles.title}
            />
          </div>
          <>
            <Row justifyContent={RowContent.spaceBetween}>
              <Typography
                variant={TypographyVariant.label}
                text={'Fees'}
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
                text={'ETA'}
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
                text={'Exchange'}
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
                text={'Final cost'}
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
                text={`1/2 approvals required`}
                className={styles.message}
              />
            </div>
          </>
        </div>
      </div>
    </div>
  )
}
