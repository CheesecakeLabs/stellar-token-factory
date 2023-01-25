import { Header } from './components/header'
import { ListPayees } from './components/list-payees'
import { Footer } from 'components/molecules'

import styles from './styles.module.scss'

export const Home: React.FC = () => {
  return (
    <main>
      <div className={styles.container}>
        <Header />
        <ListPayees />
      </div>
      <Footer />
    </main>
  )
}
