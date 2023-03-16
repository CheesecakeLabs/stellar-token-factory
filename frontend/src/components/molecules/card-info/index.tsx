import { FunctionComponent } from 'react'
import { Card } from '@stellar/design-system'

import styles from './styles.module.scss'

export interface ICardInfoProps {
  label: string
  value: number | undefined
  description?: string
}

const CardInfo: FunctionComponent<ICardInfoProps> = ({
  label,
  value,
  description,
}) => {
  return (
    <div className={styles.container}>
      <Card variant={Card.variant.highlight}>
        <div className={styles.label}>{label}</div>
        <div className={styles.value}>{value || 'Not available'}</div>
        {description && <div className={styles.description}>{description}</div>}
      </Card>
    </div>
  )
}

export { CardInfo }
