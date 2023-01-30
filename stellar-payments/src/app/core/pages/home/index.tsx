import { useEffect } from 'react'

import { usePayees } from 'services/hooks/usePayees'

import { Header } from './components/header'
import { ListPayees } from './components/list-payees'
import { Footer } from 'components/molecules'

import styles from './styles.module.scss'

export const Home: React.FC = () => {
  const { getPayees, loading, payees } = usePayees()

  useEffect(() => {
    getPayees()
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <main>
      <div className={styles.container}>
        <Header />
        <ListPayees loading={loading} payees={payees} />
      </div>
      <Footer />
    </main>
  )
}
