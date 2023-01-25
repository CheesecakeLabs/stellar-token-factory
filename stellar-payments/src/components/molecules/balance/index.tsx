import { Typography, TypographyVariant } from 'components/atoms'
import { BalanceIcon } from 'components/icons'

import styles from './styles.module.scss'

export const Balance: React.FC = () => {
  return (
    <div className={styles.container}>
      <BalanceIcon width={24} height={24} />
      <Typography
        variant={TypographyVariant.p}
        text={'€ 1,000,000.00'}
        className={styles.balanceText}
      />
    </div>
  )
}
