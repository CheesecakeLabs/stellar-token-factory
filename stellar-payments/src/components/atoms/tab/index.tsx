import { ReactNode } from 'react'

import classNames from 'classnames'

import styles from './styles.module.scss'

interface ITabProps {
  title: string
  isActived: boolean
  icon: ReactNode
  onClick(): void
}

export const Tab: React.FC<ITabProps> = ({
  title,
  isActived,
  icon,
  onClick,
}) => {
  return (
    <div
      className={classNames(
        styles.container,
        isActived ? styles.active : styles.disabled
      )}
      onClick={onClick}
    >
      {icon}
      {title}
    </div>
  )
}
