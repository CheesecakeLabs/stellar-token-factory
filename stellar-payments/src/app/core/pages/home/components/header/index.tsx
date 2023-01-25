import { useEffect } from 'react'

import { useAccount } from 'services/hooks/useAccount'

import { Typography, TypographyVariant } from 'components/atoms'
import { Account, Balance } from 'components/molecules'

import { ReactComponent as StellarLogo } from '../../../../../core/resources/stellar.svg'
import styles from './styles.module.scss'

export const Header: React.FC = () => {
  const { getBalance, loading, balance } = useAccount()

  useEffect(() => {
    getBalance()
  }, [getBalance])

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
          <Balance balance={balance} loading={loading} />
        </div>
      </div>
    </div>
  )
}
