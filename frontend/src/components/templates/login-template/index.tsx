import { Button, Card, Input, Layout } from '@stellar/design-system'

import styles from './styles.module.scss'
import '@stellar/design-system/build/styles.min.css'
import 'react-tabs/style/react-tabs.css'
import { useState } from 'react'
import { defaultLogin } from './constants'
import { Authentication, AuthStatus } from 'app/core/auth'
import { useNavigate } from 'react-router-dom'
import { CustomError } from 'components/atoms'

const LoginTemplate = (): JSX.Element => {
  const [inputs, setInputs] = useState(defaultLogin)
  const [isLoading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const navigate = useNavigate()

  const handleChange = (event: {
    target: { name: string; value: string }
  }): void => {
    setError('')
    const name = event.target.name
    const value = event.target.value
    setInputs(values => ({ ...values, [name]: value }))
  }

  const handleLogin = (): void => {
    setLoading(true)
    Authentication.login(inputs.username, inputs.password)
      .then(response => {
        if (response) {
          Authentication.setAuthenticated(AuthStatus.Authenticated)
          navigate('/')
          return
        }
        setError('Incorrect username or password')
      })
      .catch(() => {
        setError('An error occurred while logging in')
      })
      .finally(() => setLoading(false))
  }

  return (
    <main className={styles.main}>
      <Layout.Header hasDarkModeToggle projectTitle="Token Factory" />
      <Layout.Content>
        <Layout.Inset>
          <div className={styles.content}>
            <Card variant={Card.variant.highlight}>
              <Input
                id="input-username"
                name="username"
                placeholder="Username"
                onChange={handleChange}
                autoComplete="off"
              />
              <br />
              <Input
                id="input-password"
                name="password"
                placeholder="Password"
                onChange={handleChange}
                autoComplete="off"
                type={'password'}
              />
              <br />
              <Button fullWidth onClick={handleLogin} isLoading={isLoading}>
                Login
              </Button>
              <br />
              {error && <CustomError message={error} />}
            </Card>
          </div>
        </Layout.Inset>
      </Layout.Content>
    </main>
  )
}

export { LoginTemplate }
