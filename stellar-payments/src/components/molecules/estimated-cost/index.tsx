import {
  Row,
  RowContent,
  Typography,
  TypographyVariant,
} from 'components/atoms'

import styles from './styles.module.scss'

export const EstimatedCost: React.FC = () => {
  return (
    <div className={styles.container}>
      <Row justifyContent={RowContent.spaceBetween}>
        <Typography
          variant={TypographyVariant.label}
          text={'Payment amount'}
          className={styles.label}
        />
        <Typography
          variant={TypographyVariant.p}
          text={'$ 1,000.00'}
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
          text={'$ 2.47'}
          className={styles.value}
        />
      </Row>
      <div className={styles.divider}/>
      <Row justifyContent={RowContent.spaceBetween}>
        <Typography
          variant={TypographyVariant.label}
          text={'Total'}
          className={styles.label}
        />
        <Typography
          variant={TypographyVariant.p}
          text={'$ 997.53'}
          className={styles.value}
        />
      </Row>
    </div>
  )
}
