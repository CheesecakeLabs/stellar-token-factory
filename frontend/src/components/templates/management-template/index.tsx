import { Layout } from '@stellar/design-system'
import styles from './styles.module.scss'

import '@stellar/design-system/build/styles.min.css'
import 'react-tabs/style/react-tabs.css'
import { useLocation } from 'react-router-dom'
import { useCallback, useEffect, useState } from 'react'
import { CustomError } from 'components/atoms'
import { TabsManagement } from 'components/organisms'
import { ManagementHeader } from 'components/molecules'
import { FactoryService } from 'services/factory'

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

  return (
    <main className={styles.main}>
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
            />
          )}
        </Layout.Inset>
      </Layout.Content>
      <Layout.Footer />
    </main>
  )
}

export { ManagementTemplate }
