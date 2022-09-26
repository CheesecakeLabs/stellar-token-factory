import styles from './styles.module.scss'
import { Loader } from '@stellar/design-system'

const CustomLoader = (): JSX.Element => {
  return (
    <div className={styles.customLoader}>
      <Loader size="3rem" />
    </div>
  )
}

export { CustomLoader }
