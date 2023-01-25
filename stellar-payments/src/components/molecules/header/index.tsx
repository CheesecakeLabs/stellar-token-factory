import { Typography, TypographyVariant } from 'components/atoms'

import { ReactComponent as StellarLogo } from '../../../app/core/resources/stellar.svg'

import { Account } from '../account'
import { Balance } from '../balance'
import styles from './styles.module.scss'

export const Header: React.FC = () => {
  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className={styles.containerTop}>
          <StellarLogo width={128} height={64} className={styles.logo} />
          <Account />
        </div>
        <div className={styles.containerData}>
          <Typography
            variant={TypographyVariant.p}
            text={'Payments > Payees'}
            className={styles.moduleText}
          />
          <Balance />
        </div>
      </div>
    </div>
  )
}
