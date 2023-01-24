import { ListPayees } from './components/list-payees'
import { Fotter, Header } from 'components/molecules'

import styles from './styles.module.scss'

const Home = (): JSX.Element => {
  return (
    <main>
      <div className={styles.container}>
        <Header />
        <ListPayees />
      </div>
      <Fotter />
    </main>
  )
}

export default Home
