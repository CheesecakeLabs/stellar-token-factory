import { ReactNode, useRef } from 'react'

import { CloseIcon } from 'components/icons'

import { Typography, TypographyVariant } from '../typography'
import styles from './styles.module.scss'

interface IModalProps {
  isOpen: boolean
  children: ReactNode
  handleClose(): void
}

export const Modal: React.FC<IModalProps> = ({
  isOpen,
  children,
  handleClose,
}) => {
  const myRef = useRef(null)

  return (
    <>
      {isOpen && (
        <div className={styles.container}>
          <div className={styles.darkBG} onClick={handleClose} />
          <div className={styles.centered}>
            <div className={styles.modal} ref={myRef}>
              <div className={styles.header}>
                <Typography
                  variant={TypographyVariant.label}
                  text={'Titulo'}
                  className={styles.title}
                />
                <CloseIcon width={20} height={20} onClick={handleClose} />
              </div>
              {children}
            </div>
          </div>
        </div>
      )}
    </>
  )
}
