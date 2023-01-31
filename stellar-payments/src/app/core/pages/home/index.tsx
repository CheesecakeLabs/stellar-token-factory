import { useEffect, useState } from 'react'

import { usePayees } from 'services/hooks/usePayees'
import { usePayment } from 'services/hooks/usePayment'

import { Header } from './components/header'
import { ListPayees } from './components/list-payees'
import { ListPayments } from './components/list-payments'
import { Settings } from './components/settings'
import { Footer } from 'components/molecules'

import { AuthService } from 'app/core/auth/auth-service'

import styles from './styles.module.scss'

export const Home: React.FC = () => {
  const { getPayees, loading, payees } = usePayees()
  const { getLocalPayments, localPayments } = usePayment()
  const [tab, setTab] = useState(0)

  useEffect(() => {
    getPayees()
  }, [getPayees])

  useEffect(() => {
    getLocalPayments(AuthService.currentUser().email)
  }, [getLocalPayments])

  const steps = [
    <ListPayments loading={loading} payments={localPayments} payees={payees} />,
    <ListPayees loading={loading} payees={payees} />,
    <Settings />,
  ]

  return (
    <main>
      <div className={styles.container}>
        <Header tab={tab} setTab={setTab} />
        {steps[tab]}
      </div>
      <Footer />
    </main>
  )
}
