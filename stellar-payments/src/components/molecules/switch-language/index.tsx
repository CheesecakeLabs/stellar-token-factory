import { useTranslation } from 'react-i18next'

import SpainFlag from '../../../app/core/resources/spain_flag.png'
import UnitedKingdomFlag from '../../../app/core/resources/united_kingdom_flag.png'

import styles from './styles.module.scss'

export const SwitchLanguage: React.FC = () => {
  const { i18n } = useTranslation()

  return (
    <div className={styles.container}>
      <img
        src={UnitedKingdomFlag}
        width="24px"
        height="24px"
        onClick={(): void => {
          i18n.changeLanguage('en')
        }}
        style={i18n.language == 'en' ? { opacity: 1 } : { opacity: 0.5 }}
      />
      <img
        src={SpainFlag}
        width="24px"
        height="24px"
        onClick={(): void => {
          i18n.changeLanguage('es')
        }}
        style={i18n.language == 'es' ? { opacity: 1 } : { opacity: 0.5 }}
      />
    </div>
  )
}
