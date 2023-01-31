import { Dispatch, SetStateAction, useEffect } from 'react'

import { HomeOutlined, TeamOutlined } from '@ant-design/icons'
import { Row } from 'antd'
import { useAccount } from 'services/hooks/useAccount'

import { Tab } from 'components/atoms/tab'
import { Account, Balance } from 'components/molecules'

import { ReactComponent as StellarLogo } from '../../../../../core/resources/stellar.svg'
import styles from './styles.module.scss'

interface IHeaderProps {
  tab: number
  setTab: Dispatch<SetStateAction<number>>
}

export const Header: React.FC<IHeaderProps> = ({ tab, setTab }) => {
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
          <Row>
            <Tab
              title="Payments"
              icon={<HomeOutlined />}
              isActived={tab == 0}
              onClick={(): void => setTab(0)}
            />
            <Tab
              title="Payees"
              icon={<TeamOutlined />}
              isActived={tab == 1}
              onClick={(): void => setTab(1)}
            />
          </Row>
          <Balance balance={balance} loading={loading} />
        </div>
      </div>
    </div>
  )
}
