import { useState } from 'react'
import { useHistory } from 'react-router-dom'

import { message } from 'antd'
import { useAccount } from 'services/hooks/useAccount'

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
  const { signIn, loading } = useAccount()
  const [inputs, setInputs] = useState<Hooks.UseAccountTypes.ISignIn>({
    email: '',
    password: '',
  })

  const handleChange = (event: {
    target: { name: string; value: string }
  }): void => {
    const name = event.target.name
    const value = event.target.value
    setInputs(values => ({ ...values, [name]: value }))
  }

  const login = async (): Promise<void> => {
    await signIn({
      email: inputs.email,
      password: inputs.password,
    }).then(isSuccess => {
      if (isSuccess) {
        return history.push('/')
      }
      message.error('Unauthenticated user!')
    })
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
        onClick={login}
        isLoading={loading}
        isDisabled={!inputs.email || !inputs.password}
      />
    </div>
  )
}
