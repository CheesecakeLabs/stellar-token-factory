import {
  Dispatch,
  FunctionComponent,
  SetStateAction,
  useCallback,
  useEffect,
  useState,
} from 'react'

import { TabsManagementEnum } from 'components/templates'
import { Column, CustomError, LastUpdated, Row } from 'components/atoms'
import { CardInfo } from 'components/molecules'
import { ChartGeneral } from './chart-general'
import { ListHolders } from './list-holders'
import { FactoryService } from 'services/factory'
import { IGeneralInfo } from 'services/factory/interfaces'

export interface IGeneralProps {
  distribution: string
  assetCode: string
  issuer: string
  setShowHelper: Dispatch<SetStateAction<TabsManagementEnum | undefined>>
}

const General: FunctionComponent<IGeneralProps> = () => {
  const [isLoading, setLoading] = useState(false)
  const [generalInfo, setGeneralInfo] = useState<IGeneralInfo>()
  const [error, setError] = useState<string>()

  const getData = useCallback(() => {
    setLoading(true)
    FactoryService.getGeneralInfo()
      .then(response => {
        setGeneralInfo(response.data)
      })
      .catch(() => {
        setError('An error occurred while loading the informations')
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    getData()
  }, [getData])

  return (
    <>
      {error ? (
        <CustomError message={error} />
      ) : (
        <div>
          <Row>
            <Column col={4}>
              <CardInfo
                label={'Total supply'}
                value={generalInfo?.total_supply}
                description={'COIN'}
              />
              <CardInfo
                label={'Total in-circulation'}
                value={generalInfo?.total_in_circulation}
                description={'COIN'}
              />
              <CardInfo
                label={'Total trustlines'}
                value={generalInfo?.total_trustlines}
              />
              <CardInfo
                label={'Total reserves'}
                value={generalInfo?.total_reserves}
              />
            </Column>
            <Column col={8}>
              <ChartGeneral label={'Total supply and Distributor supply'} />
              <ListHolders
                isLoading={isLoading}
                data={generalInfo?.top_holders || []}
              />
            </Column>
          </Row>
          <LastUpdated date={generalInfo?.last_updated} />
        </div>
      )}
    </>
  )
}

export { General }
