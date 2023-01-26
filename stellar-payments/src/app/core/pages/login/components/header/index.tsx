import { ReactComponent as StellarLogo } from '../../../../../core/resources/stellar.svg'
import styles from './styles.module.scss'

export const Header: React.FC = () => {
  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className={styles.containerTop}>
          <StellarLogo width={128} height={64} className={styles.logo} />
        </div>
      </div>
    </div>
  )
}
