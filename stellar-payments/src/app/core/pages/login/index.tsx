import { Header } from './components/header'
import { LoginModal } from './components/login-modal'
import { Footer } from 'components/molecules'

import styles from './styles.module.scss'

export const Login: React.FC = () => {
  return (
    <main>
      <div className={styles.container}>
        <Header />
        <LoginModal />
      </div>
      <Footer />
    </main>
  )
}
