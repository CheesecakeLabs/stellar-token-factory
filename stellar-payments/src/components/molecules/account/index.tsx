import { useHistory } from 'react-router-dom'

import { MailFilled, NotificationFilled, UserOutlined } from '@ant-design/icons'

import { Typography, TypographyVariant } from 'components/atoms'

import { Authentication } from 'app/core/auth'
import { AuthService } from 'app/core/auth/auth-service'

import styles from './styles.module.scss'

export const Account: React.FC = () => {
  const history = useHistory()

  function logout(): void {
    Authentication.logout()
    history.push('/login')
  }

  return (
    <div className={styles.container}>
      <div className={styles.account}>
        <MailFilled
          style={{ fontSize: '16px', color: '#ffffff', marginRight: '1rem' }}
        />
        <NotificationFilled
          style={{ fontSize: '16px', color: '#ffffff', marginRight: '3rem' }}
        />
        <UserOutlined style={{ fontSize: '16px', color: '#ffffff' }} />
        <Typography
          variant={TypographyVariant.label}
          text={AuthService.currentUser().name}
          className={styles.userText}
        />
        <div onClick={logout}>
          <Typography
            variant={TypographyVariant.label}
            text={'Log out'}
            className={styles.logout}
          />
        </div>
      </div>
    </div>
  )
}
