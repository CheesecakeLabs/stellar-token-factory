import { SwitchLanguage } from '..'
import styles from './styles.module.scss'

export const Footer: React.FC = () => {
  return (
    <footer className={styles.container}>
      © {new Date().getFullYear()} Cheesecake Labs, Inc.
      <SwitchLanguage />
    </footer>
  )
}
