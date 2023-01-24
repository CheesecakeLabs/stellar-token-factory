import { Typography, TypographyVariant } from 'components/atoms'
import { ArrowDown, BalanceIcon, UserIcon } from 'components/icons'

import { ReactComponent as StellarLogo } from '../../../app/core/resources/stellar.svg'

import styles from './styles.module.scss'

export const Header: React.FC = () => {
  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className={styles.containerTop}>
          <StellarLogo width={128} height={64} />
          <div className={styles.account}>
            <UserIcon width={14} height={16} />
            <Typography
              variant={TypographyVariant.label}
              text={'User 1'}
              className={styles.userText}
            />
            <ArrowDown width={12} height={12} />
          </div>
        </div>
        <div className={styles.containerBalance}>
          <BalanceIcon width={32} height={32} />
          <Typography
            variant={TypographyVariant.p}
            text={'€ 1,000,000.00'}
            className={styles.balanceText}
          />
        </div>
        <Typography
          variant={TypographyVariant.p}
          text={'Payments > Payees'}
          className={styles.moduleText}
        />
      </div>
    </div>
  )
}
