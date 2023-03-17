import { Layout } from '@stellar/design-system'
import styles from './styles.module.scss'

import '@stellar/design-system/build/styles.min.css'
import 'react-tabs/style/react-tabs.css'
import { useLocation } from 'react-router-dom'
import { ReactNode, useCallback, useEffect, useState } from 'react'
import { CustomError } from 'components/atoms'
import { TabsManagement } from 'components/organisms'
import { ManagementHeader } from 'components/molecules'
import { FactoryService } from 'services/factory'
import { HelperMint } from './components/helper-mint'
import { HelperBurn } from './components/helper-burn'
import { HelperTransfer } from './components/helper-transfer'
import { HelperHomeDomain } from './components/helper-home-domain'
import { HelperToml } from './components/helper-toml'
import { HelperFreeze } from './components/helper-freeze'
import { HelperClawback } from './components/helper-clawback'

export enum TabsManagementEnum {
  MINT = 'Mint',
  BURN = 'Burn',
  TRANSFER = 'Transfer',
  HOME_DOMAIN = 'Home Domain',
  TOML = 'TOML',
  FREEZE = 'Freeze',
  CLAWBACK = 'Clawback',
}

type LocationState = {
  state: {
    asset_code: string
    asset_issuer: string
    clawback: boolean
    freeze: boolean
  }
}

const ManagementTemplate = (): JSX.Element => {
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [assetDistributor, setAssetDistributor] = useState('')
  const location = useLocation()
  const [showHelper, setShowHelper] = useState<TabsManagementEnum>()
  const [isDarkMode, setMode] = useState<boolean>()

  const { state } = location as LocationState

  const loadAssetDistributor = useCallback(() => {
    setIsLoading(true)
    FactoryService.getAssetDistributor(state.asset_code, state.asset_issuer)
      .then(response => {
        setAssetDistributor(response.data.public_key)
      })
      .catch(() => {
        setError('Unable to retrieve Distribution account')
      })
      .finally(() => {
        setIsLoading(false)
      })
  }, [state.asset_code, state.asset_issuer])

  useEffect(() => {
    loadAssetDistributor()
  }, [state, loadAssetDistributor])

  const helperPanel = (): ReactNode | undefined => {
    if (showHelper == TabsManagementEnum.MINT) {
      return <HelperMint setShowHelper={setShowHelper} />
    }
    if (showHelper == TabsManagementEnum.BURN) {
      return <HelperBurn setShowHelper={setShowHelper} />
    }
    if (showHelper == TabsManagementEnum.TRANSFER) {
      return <HelperTransfer setShowHelper={setShowHelper} />
    }
    if (showHelper == TabsManagementEnum.HOME_DOMAIN) {
      return <HelperHomeDomain setShowHelper={setShowHelper} />
    }
    if (showHelper == TabsManagementEnum.TOML) {
      return <HelperToml setShowHelper={setShowHelper} />
    }
    if (showHelper == TabsManagementEnum.FREEZE) {
      return <HelperFreeze setShowHelper={setShowHelper} />
    }
    if (showHelper == TabsManagementEnum.CLAWBACK) {
      return <HelperClawback setShowHelper={setShowHelper} />
    }
  }

  return (
    <main className={styles.main}>
      {helperPanel()}
      <Layout.Header
        hasDarkModeToggle
        projectTitle="Stellar Asset Sandbox"
        projectLink=""
        contentCenter={
          <ManagementHeader
            asset_issuer={state?.asset_issuer}
            asset_code={state?.asset_code}
            asset_distributor={assetDistributor}
            isLoading={isLoading}
          />
        }
        onDarkModeToggleEnd={(isDarkMode: boolean): void => {
          setMode(isDarkMode)
        }}
      />
      <Layout.Content>
        <Layout.Inset>
          {error ? (
            <CustomError message={error} />
          ) : (
            <TabsManagement
              distribution={assetDistributor}
              issuer={state?.asset_issuer}
              assetCode={state?.asset_code}
              isLoading={isLoading}
              isFreeze={state?.freeze}
              isClawback={state?.clawback}
              setShowHelper={setShowHelper}
              isDarkMode={isDarkMode}
            />
          )}
        </Layout.Inset>
      </Layout.Content>
      <Layout.Footer />
    </main>
  )
}

export { ManagementTemplate }
