import { FunctionComponent } from 'react'
import styles from './styles.module.scss'

export interface ICustomTagProps {
  message: string
  tooltip: string
}

const CustomTag: FunctionComponent<ICustomTagProps> = props => {
  return (
    <div className={styles.readOnly}>
      <span title={props.tooltip}>{props.message}</span>
    </div>
  )
}

export { CustomTag }
