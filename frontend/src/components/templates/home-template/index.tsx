import { Card, Layout } from '@stellar/design-system'
import { useNavigate } from 'react-router-dom'
import { useCallback, useState } from 'react'
import { isConnected, getPublicKey } from '@stellar/freighter-api'
import { CustomLoader, NetworkStatus } from 'components/atoms'
import { CustomError } from 'components/atoms/custom-error'
import { InputKey } from 'components/molecules'

import styles from './styles.module.scss'
import '@stellar/design-system/build/styles.min.css'
import 'react-tabs/style/react-tabs.css'
import { FactoryService } from 'services/factory'
import { messageError } from 'services/factory/constants'

const HomeTemplate = (): JSX.Element => {
  const navigate = useNavigate()
  const [publicKey, setPublicKey] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handlePublicKey = useCallback(
    async (publicKey: string) => {
      setPublicKey(publicKey)
      setError('')

      if (publicKey.length != 56) return

      setIsLoading(true)
      FactoryService.getIssuerInfo(publicKey)
        .then(response => {
          if (publicKey.length == 56) {
            navigate('/factory', {
              state: {
                publicKey: publicKey,
                data: response.data,
              },
            })
          }
        })
        .catch(result => {
          const code = result?.response?.data?.code
          setError(
            messageError.get(code) || 'Could not communicate with the server'
          )
        })
        .finally(() => {
          setIsLoading(false)
        })
    },
    [navigate]
  )

  const getKey = useCallback(() => {
    getPublicKey().then(publicKey => {
      handlePublicKey(publicKey)
    })
  }, [handlePublicKey])

  const handleChange = (event: { target: { value: string } }): void => {
    handlePublicKey(event.target.value)
  }

  return (
    <main className={styles.main}>
      <Layout.Header
        hasDarkModeToggle
        projectTitle="Token Factory"
        contentRight={<NetworkStatus key={'status'} />}
      />
      <Layout.Content>
        <Layout.Inset>
          <Card variant={Card.variant.highlight}>
            {isConnected() ? (
              <div>
                {isLoading ? (
                  <CustomLoader />
                ) : (
                  <InputKey
                    publicKey={publicKey}
                    getKey={getKey}
                    handleChange={handleChange}
                  />
                )}
              </div>
            ) : (
              <p className={styles.message}>
                You are not connected to Freighter!
              </p>
            )}
            {error ? <CustomError message={error} /> : <div />}
          </Card>
        </Layout.Inset>
      </Layout.Content>
      <Layout.Footer />
    </main>
  )
}

export { HomeTemplate }
