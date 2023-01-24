import styles from './styles.module.scss'

export const Fotter: React.FC = () => {
  return (
    <footer className={styles.container}>
      © {new Date().getFullYear()} Cheesecake Labs, Inc.
    </footer>
  )
}
