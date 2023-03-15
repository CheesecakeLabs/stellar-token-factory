import { Dispatch, FunctionComponent, SetStateAction } from 'react'

import styles from './styles.module.scss'
import { TabsManagementEnum } from 'components/templates'
import { CardInfo } from '../card-info'
import { Column } from 'components/atoms'

export interface IGeneralProps {
  distribution: string
  assetCode: string
  issuer: string
  setShowHelper: Dispatch<SetStateAction<TabsManagementEnum | undefined>>
}

const General: FunctionComponent<IGeneralProps> = props => {
  return (
    <div>
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
    </div>
  )
}

export { General }
