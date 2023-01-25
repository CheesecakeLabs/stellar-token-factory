import { MailFilled, NotificationFilled, UserOutlined } from '@ant-design/icons'

import { Typography, TypographyVariant } from 'components/atoms'

import styles from './styles.module.scss'

export const Account: React.FC = () => {
  return (
    <div className={styles.container}>
      <div className={styles.account}>
        <MailFilled
          style={{ fontSize: '16px', color: '#ffffff', marginRight: '1rem' }}
        />
        <NotificationFilled
          style={{ fontSize: '16px', color: '#ffffff', marginRight: '3rem' }}
        />
        <UserOutlined
          style={{ fontSize: '16px', color: '#ffffff'}}
        />
        <Typography
          variant={TypographyVariant.label}
          text={'Channel'}
          className={styles.userText}
        />
        <Typography
          variant={TypographyVariant.label}
          text={'Log out'}
          className={styles.logout}
        />
      </div>
    </div>
  )
}
