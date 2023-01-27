import { CheckCircleFilled } from '@ant-design/icons'

import { Typography, TypographyVariant } from 'components/atoms'

import styles from './styles.module.scss'

export const StatusTransaction: React.FC = () => {
  return (
    <div className={styles.container}>
      <CheckCircleFilled style={{ fontSize: '2rem', color: '#16a085' }} />
      <Typography
        variant={TypographyVariant.label}
        text={'Success! You have made the payment of $999.00'}
        className={styles.statusMessage}
      />
    </div>
  )
}
