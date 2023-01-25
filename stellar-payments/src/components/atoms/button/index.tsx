import { ReactNode } from 'react'

import classNames from 'classnames'

import { LoadingIcon } from 'components/icons'

import styles from './styles.module.scss'

export enum ButtonVariant {
  primary = 'primary',
  secondary = 'secondary',
  tertiary = 'tertiary',
  login = 'login',
  icon = 'icon',
}

export interface IButtonProps {
  variant: ButtonVariant
  label: string
  onClick?: () => void
  icon?: ReactNode
  isDisabled?: boolean
  isExpanded?: boolean
  message?: string
  isLoading?: boolean
  removeSideMargin?: boolean
}

const Button = (props: IButtonProps): JSX.Element => {
  return (
    <button
      onClick={props.onClick}
      className={classNames(
        styles.button,
        styles[props.variant],
        props.removeSideMargin ? styles.removeSideMargin : undefined
      )}
      disabled={props.isDisabled}
    >
      {props.isLoading ? (
        <LoadingIcon width={14} height={14} />
      ) : (
        <>
          <div className={styles.row}>
            {props.icon && props.icon}
            {props.label}
          </div>
          {props.message && (
            <div className={styles.message}>{props.message}</div>
          )}
        </>
      )}
    </button>
  )
}

export { Button }
