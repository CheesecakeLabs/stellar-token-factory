import { useTranslation } from 'react-i18next'

import { toEur } from 'services/utils/utils'

import { Typography, TypographyVariant } from 'components/atoms'
import { BalanceIcon } from 'components/icons'

import styles from './styles.module.scss'

interface IBalanceProps {
  balance: Hooks.UseAccountTypes.IBalance | undefined
  loading: boolean
}

export const Balance: React.FC<IBalanceProps> = ({ balance, loading }) => {
  const { t } = useTranslation()

  return (
    <div className={styles.container}>
      <BalanceIcon width={24} height={24} />
      <Typography
        variant={TypographyVariant.p}
        text={loading || !balance ? t('loading') : `${toEur(balance.balance)}`}
        className={styles.balanceText}
      />
    </div>
  )
}
