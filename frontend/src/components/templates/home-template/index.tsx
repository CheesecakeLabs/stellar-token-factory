import { Button, Card, Layout } from '@stellar/design-system'
import { useNavigate } from 'react-router-dom'
import { useCallback, useState } from 'react'
import { isConnected, getPublicKey, getNetwork } from '@stellar/freighter-api'
import { CustomLoader, HeaderStatus } from 'components/atoms'
import { CustomError } from 'components/atoms/custom-error'
import { InputKey } from 'components/molecules'

import styles from './styles.module.scss'
import '@stellar/design-system/build/styles.min.css'
import 'react-tabs/style/react-tabs.css'
import { FactoryService } from 'services/factory'
import { messageError } from 'services/factory/constants'
import { Download } from 'react-feather'
import { HelperHome } from './components/helper-home'

const HomeTemplate = (): JSX.Element => {
  const navigate = useNavigate()
  const [publicKey, setPublicKey] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [showHelper, setShowHelper] = useState(false)

  const handlePublicKey = useCallback(
    async (publicKey: string) => {
      setPublicKey(publicKey)
      setError('')

      if (publicKey.length != 56) return
      setIsLoading(true)
      if (!(await isValidNetwork())) return

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

  const isValidNetwork = async (): Promise<boolean> => {
    const envNetwork = process.env.REACT_APP_NETWORK
    const isValid = !envNetwork || envNetwork == (await getNetwork())
    if (!isValid) {
      setError(`The network must be ${envNetwork}`)
      setIsLoading(false)
    }
    return isValid
  }

  const openExtension = (): void => {
    window.open(
      'https://chrome.google.com/webstore/detail/freighter/bcacfldlkkdogcmkkibnjlakofdplcbk',
      '_blank'
    )
  }

  return (
    <main className={styles.main}>
      {showHelper && <HelperHome setShowHelper={setShowHelper} />}
      <Layout.Header
        hasDarkModeToggle
        projectTitle="Stellar Asset Sandbox"
        projectLink=""
        contentRight={<HeaderStatus key={'status'} />}
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
                    setShowHelper={setShowHelper}
                  />
                )}
              </div>
            ) : (
              <div className={styles.warning}>
                <p className={styles.message}>
                  You are not connected to Freighter!
                </p>
                <Button onClick={openExtension}>
                  Get Freighter extension <Download />
                </Button>
              </div>
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
