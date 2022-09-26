import { FunctionComponent } from 'react'
import { InfoBlock } from '@stellar/design-system'
import styles from './styles.module.scss'

export interface ITokenMessageProps {
  hash: string
  link: string
}

const TokenMessage: FunctionComponent<
  ITokenMessageProps
> = tokenMessageProps => {
  return (
    <div className={styles.content}>
      {tokenMessageProps.hash || tokenMessageProps.link ? (
        <InfoBlock variant={InfoBlock.variant.success}>
          <div>
            <p>Operation completed successfully!</p>
            <p>Hash: {tokenMessageProps.hash}</p>
            <p>
              Transaction link:
              <a href={tokenMessageProps.link} target="_blank">
                {tokenMessageProps.link}
              </a>
            </p>
          </div>
        </InfoBlock>
      ) : (
        <div />
      )}
    </div>
  )
}

export { TokenMessage }
