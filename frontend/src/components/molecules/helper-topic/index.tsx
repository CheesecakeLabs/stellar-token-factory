import { FunctionComponent, ReactNode } from 'react'
import styles from './styles.module.scss'

export interface IHelperTopicProps {
  title: string
  children: ReactNode
}

const HelperTopic: FunctionComponent<IHelperTopicProps> = ({
  title,
  children,
}) => {
  return (
    <div className={styles.container}>
      <div className={styles.topic}>{title}</div>
      <div className={styles.content}>{children}</div>
    </div>
  )
}

export { HelperTopic }
