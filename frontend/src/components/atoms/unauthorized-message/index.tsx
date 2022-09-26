import { FunctionComponent } from 'react'
import styles from './styles.module.scss'
import { Lock } from 'react-feather'

export interface IUnauthorizedMessageProps {
  message: string
}

const UnauthorizedMessage: FunctionComponent<IUnauthorizedMessageProps> = props => {
  return (
    <div className={styles.content}>
      <Lock size={32}/>
      <p>{props.message}</p>
    </div>
  )
}

export { UnauthorizedMessage }
