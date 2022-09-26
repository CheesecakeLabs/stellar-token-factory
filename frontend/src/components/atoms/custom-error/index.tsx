import { FunctionComponent } from 'react'
import { InfoBlock } from '@stellar/design-system'
import styles from './styles.module.scss'

export interface ICustomErrorProps {
  message: string
}

const CustomError: FunctionComponent<ICustomErrorProps> = customErrorProps => {
  return (
    <div className={styles.content}>
      <InfoBlock variant={InfoBlock.variant.error}>
        {customErrorProps.message}
      </InfoBlock>
    </div>
  )
}

export { CustomError }
