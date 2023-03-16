import { Button, Card, Layout } from '@stellar/design-system'
import { useNavigate, useLocation } from 'react-router-dom'
import { ListAssets } from 'components/molecules'
import { FormToken, SettingsModal } from 'components/organisms'
import { ReactNode, useCallback, useEffect, useState } from 'react'

import styles from './styles.module.scss'
import '@stellar/design-system/build/styles.min.css'
import { CustomError, HeaderStatus } from 'components/atoms'
import { IAssetProps, IIssuerInfo } from 'services/factory/interfaces'
import { FactoryService } from 'services/factory'
import { HelperAssets } from './components/helper-assets'
import { HelperForging } from './components/helper-forging'
import { HelperSettings } from './components/helper-settings'

type LocationState = {
  state: {
    publicKey: string
    data: IAssetProps[]
  }
}

export enum HelperFactoryEnum {
  SETTINGS = 'Settings',
  FORGING = 'Forging',
  ASSETS = 'Assets',
}

const FactoryTemplate = (): JSX.Element => {
  const navigate = useNavigate()
  const location = useLocation()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const { state } = location as LocationState
  const [isModalVisible, setModalVisible] = useState(false)
  const [issuerInfo, setIssuerInfo] = useState<IIssuerInfo>()
  const [showHelper, setShowHelper] = useState<HelperFactoryEnum>()

  const redirectHome = useCallback(() => {
    navigate('/home')
  }, [navigate])

  const loadTokens = useCallback(() => {
    setIsLoading(true)
    FactoryService.getIssuerInfo(state?.publicKey)
      .then(response => {
        setIssuerInfo(response.data)
      })
      .catch(() => {
        setError('Could not update asset listing at this time')
      })
      .finally(() => {
        setIsLoading(false)
      })
  }, [state])

  useEffect(() => {
    if (!state) {
      redirectHome()
    }
    loadTokens()
  }, [state, redirectHome, loadTokens])

  const closeModal = (): void => {
    setModalVisible(false)
  }

  const isReadOnly = (): boolean => {
    if (!issuerInfo?.assets) {
      return true
    }
    return !issuerInfo?.assets.some(e => e.issuer === state?.publicKey)
  }

  const helperPanel = (): ReactNode => {
    if (showHelper == HelperFactoryEnum.SETTINGS) {
      return <HelperSettings setShowHelper={setShowHelper} />
    }
    if (showHelper == HelperFactoryEnum.ASSETS) {
      return <HelperAssets setShowHelper={setShowHelper} />
    }
    if (showHelper == HelperFactoryEnum.FORGING) {
      return <HelperForging setShowHelper={setShowHelper} />
    }
  }

  return (
    <main className={styles.main}>
      <>
        {helperPanel()}
        <Layout.Header
          hasDarkModeToggle
          projectTitle="Stellar Asset Sandbox"
          projectLink=""
          contentRight={<HeaderStatus key={'network'} />}
        />
        <Layout.Content>
          <Layout.Inset>
            <Card variant={Card.variant.highlight}>
              <div className={styles.cardAddress}>
                <p className={styles.textAddress}>
                  Issuing: {state?.publicKey}
                </p>
                <div className={styles.issuerActions}>
                  <Button
                    variant={Button.variant.tertiary}
                    size={Button.size.small}
                    onClick={(): void => setModalVisible(true)}
                  >
                    Settings
                  </Button>
                  <Button
                    variant={Button.variant.tertiary}
                    size={Button.size.small}
                    onClick={redirectHome}
                  >
                    Change
                  </Button>
                </div>
              </div>
            </Card>
            <br />
            {error ? <CustomError message={error} /> : <div />}
            <ListAssets
              issuerInfo={issuerInfo}
              isLoading={isLoading}
              issuer={state?.publicKey}
              setShowHelper={setShowHelper}
            />
            <br />
            <FormToken
              publicKey={state?.publicKey}
              loadTokens={loadTokens}
              setShowHelper={setShowHelper}
            />
          </Layout.Inset>
        </Layout.Content>
        <Layout.Footer />
        {isModalVisible && (
          <SettingsModal
            isModalVisible={isModalVisible}
            closeModal={closeModal}
            issuer={state?.publicKey}
            isReadOnly={isReadOnly()}
            loadTokens={loadTokens}
            setShowHelper={setShowHelper}
          />
        )}
      </>
    </main>
  )
}

export { FactoryTemplate }
