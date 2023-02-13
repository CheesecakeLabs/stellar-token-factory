import { FunctionComponent, ReactNode } from 'react'
import styles from './styles.module.scss'
import { HelpCircle } from 'react-feather'
import { Button, Heading6 } from '@stellar/design-system'

export interface IHelperPanelProps {
  onClick(): void
  children: ReactNode
}

const HelperPanel: FunctionComponent<IHelperPanelProps> = ({
  onClick,
  children,
}) => {
  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.headerTitle}>
          <HelpCircle size={18} />
          <Heading6>Helper</Heading6>
        </div>
        <Button
          variant={Button.variant.secondary}
          size={Button.size.small}
          onClick={onClick}
        >
          Close
        </Button>
      </div>
      <div className={styles.content}>{children}</div>
    </div>
  )
}

export { HelperPanel }
