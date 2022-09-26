import { FunctionComponent } from 'react'
import styles from './styles.module.scss'

export interface ICustomTagProps {
  message: string
}

const CustomTag: FunctionComponent<ICustomTagProps> = props => {
  return <div className={styles.readOnly}>{props.message}</div>
}

export { CustomTag }
