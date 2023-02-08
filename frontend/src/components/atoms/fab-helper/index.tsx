import { FunctionComponent } from 'react'
import styles from './styles.module.scss'
import { HelpCircle } from 'react-feather'

export enum FabHelperVariant {
  primary = 'primary',
  secondary = 'secondary',
  fixedRight = 'fixedRight',
}

export interface IFabHelperProps {
  onClick(): void
  variant: FabHelperVariant
}

const FabHelper: FunctionComponent<IFabHelperProps> = ({
  onClick,
  variant,
}) => {
  return (
    <div className={styles[variant]} onClick={onClick}>
      <HelpCircle size={variant == FabHelperVariant.primary ? 28 : 16} />
    </div>
  )
}

export { FabHelper }
