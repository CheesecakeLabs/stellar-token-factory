import { useEffect, useState } from 'react'

import { usePayees } from 'services/hooks/usePayees'

import { Header } from './components/header'
import { ListPayees } from './components/list-payees'
import { ListPayments } from './components/list-payments'
import { Footer } from 'components/molecules'

import styles from './styles.module.scss'

export const Home: React.FC = () => {
  const { getPayees, loading, payees } = usePayees()
  const [tab, setTab] = useState(0)

  useEffect(() => {
    getPayees()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <main>
      <div className={styles.container}>
        <Header tab={tab} setTab={setTab} />
        {tab == 0 ? (
          <ListPayments loading={loading} payments={[]} />
        ) : (
          <ListPayees loading={loading} payees={payees} />
        )}
      </div>
      <Footer />
    </main>
  )
}
