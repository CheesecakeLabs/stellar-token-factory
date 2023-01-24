import { ReactNode } from 'react'

import styles from './styles.module.scss'

export enum RowContent {
  start = 'start',
  spaceBetween = 'space-between',
}

export interface IRowProps {
  children: ReactNode
  justifyContent?: RowContent
  onClick?: () => void
}

const Row = (props: IRowProps): JSX.Element => {
  return (
    <div
      className={styles.row}
      style={{ justifyContent: props.justifyContent }}
      onClick={props.onClick}
    >
      {props.children}
    </div>
  )
}

export { Row }
