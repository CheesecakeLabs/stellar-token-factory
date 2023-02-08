import { FunctionComponent, ReactNode } from 'react'
import styles from './styles.module.scss'
import { Heading6 } from '@stellar/design-system'

export interface IHelperItemProps {
  title: string
  children: ReactNode
}

const HelperItem: FunctionComponent<IHelperItemProps> = ({
  title,
  children,
}) => {
  return (
    <div className={styles.container}>
      <Heading6>{title}</Heading6>
      <p>{children}</p>
    </div>
  )
}

export { HelperItem }
