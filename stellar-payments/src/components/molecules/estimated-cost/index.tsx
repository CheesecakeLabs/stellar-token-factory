import { toEur, toUsd } from 'services/utils/utils'

import {
  Row,
  RowContent,
  Typography,
  TypographyVariant,
} from 'components/atoms'

import styles from './styles.module.scss'

interface IEstimatedCost {
  amount: number
  payment: Hooks.UsePaymentTypes.IPayment | undefined
}

export const EstimatedCost: React.FC<IEstimatedCost> = ({
  amount,
  payment,
}) => {
  return (
    <div className={styles.container}>
      <Typography
        variant={TypographyVariant.label}
        text={`Estimated transaction costs`}
        className={styles.title}
      />
      <div className={styles.containerCosts}>
        <Row justifyContent={RowContent.spaceBetween}>
          <Typography
            variant={TypographyVariant.label}
            text={'Payment amount'}
            className={styles.label}
          />
          <Typography
            variant={TypographyVariant.p}
            text={toUsd(amount)}
            className={styles.value}
          />
        </Row>
        <Row justifyContent={RowContent.spaceBetween}>
          <Typography
            variant={TypographyVariant.label}
            text={'Fees'}
            className={styles.label}
          />
          <Typography
            variant={TypographyVariant.p}
            text={'$ 0.00'}
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
            text={toEur(payment?.final_cost ?? 0)}
            className={styles.value}
          />
        </Row>
      </div>
    </div>
  )
}
