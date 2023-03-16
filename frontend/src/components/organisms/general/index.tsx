import { Dispatch, FunctionComponent, SetStateAction } from 'react'

import { TabsManagementEnum } from 'components/templates'
import { Column, Row } from 'components/atoms'
import { CardInfo, CardChartLine } from 'components/molecules'

export interface IGeneralProps {
  distribution: string
  assetCode: string
  issuer: string
  setShowHelper: Dispatch<SetStateAction<TabsManagementEnum | undefined>>
}

const General: FunctionComponent<IGeneralProps> = () => {
  return (
    <Row>
      <Column col={4}>
        <CardInfo
          label={'Total supply'}
          value={'1000,00'}
          description={'COIN'}
        />
        <CardInfo
          label={'Total in-circulation'}
          value={'980,302'}
          description={'COIN'}
        />
        <CardInfo label={'Total trustlines'} value={'7.203'} />
        <CardInfo label={'Total reserves'} value={'Not available'} />
      </Column>
      <Column col={8}>
        <CardChartLine label={'Total supply and Distributor supply'} />
      </Column>
    </Row>
  )
}

export { General }
