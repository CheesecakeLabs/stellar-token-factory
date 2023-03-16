import { FunctionComponent } from 'react'
import { formatDate } from 'utils/formatter'

import styles from './styles.module.scss'

export interface ILastUpdatedProps {
  date: number | undefined
}

const LastUpdated: FunctionComponent<ILastUpdatedProps> = ({ date }) => {
  return (
    <div className={styles.container}>
      {date
        ? `Last updated on ${formatDate(date)}`
        : 'Last update date not available'}
    </div>
  )
}

export { LastUpdated }
