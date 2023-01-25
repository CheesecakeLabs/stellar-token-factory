import { useHistory } from 'react-router-dom'

import {
  Button,
  ButtonVariant,
  InputText,
  InputTextVariant,
  Typography,
  TypographyVariant,
} from 'components/atoms'

import styles from './styles.module.scss'

export const LoginModal: React.FC = () => {
  const history = useHistory()

  const handleChange = (event: {
    target: { name: string; value: string }
  }): void => {
    const value = event.target.value
  }

  return (
    <div className={styles.container}>
      <Typography
        variant={TypographyVariant.label}
        text={'Access payment module'}
        className={styles.signInText}
      />
      <InputText
        variant={InputTextVariant.secondary}
        name={'email'}
        placeHolder={'Email'}
        handleChange={handleChange}
        type={'email'}
      />
      <InputText
        variant={InputTextVariant.secondary}
        name={'password'}
        placeHolder={'Password'}
        handleChange={handleChange}
        type={'password'}
      />
      <Button
        variant={ButtonVariant.login}
        label={'Login'}
        onClick={(): void => history.push('/home')}
      />
    </div>
  )
}
