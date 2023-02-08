import { Dispatch, FunctionComponent, SetStateAction, useCallback } from 'react'
import { Button, Card, Heading6 } from '@stellar/design-system'
import {
  CustomLoader,
  CustomTag,
  FabHelper,
  FabHelperVariant,
} from 'components/atoms'

import styles from './styles.module.scss'
import { useNavigate } from 'react-router-dom'
import { IAssetProps, IIssuerInfo } from 'services/factory/interfaces'
import { List } from 'react-feather'
import { HelperFactoryEnum } from 'components/templates'

export interface IListAssetsProps {
  issuerInfo?: IIssuerInfo
  isLoading: boolean
  issuer: string
  setShowHelper: Dispatch<SetStateAction<HelperFactoryEnum | undefined>>
}

const ListAssets: FunctionComponent<IListAssetsProps> = props => {
  const navigate = useNavigate()

  const toManagement = useCallback(
    (item: IAssetProps) => {
      navigate('/management', {
        state: {
          asset_code: item.code,
          asset_issuer: item.issuer,
          clawback: props.issuerInfo?.clawback,
          freeze: props.issuerInfo?.freeze,
        },
      })
    },
    [navigate, props]
  )

  const isReadOnly = (assetIssuer: string): boolean => {
    return props.issuer !== assetIssuer
  }

  return (
    <div className={styles.content}>
      <Card variant={Card.variant.highlight}>
        <div className={styles.row}>
          <Heading6>Assets</Heading6>
          <FabHelper
            variant={FabHelperVariant.secondary}
            onClick={(): void => props.setShowHelper(HelperFactoryEnum.ASSETS)}
          />
        </div>
        {props.isLoading ? (
          <CustomLoader />
        ) : props.issuerInfo && props.issuerInfo?.assets.length > 0 ? (
          <table>
            <tbody>
              <tr className={styles.tableHeader}>
                <td className={styles.tdSymbol}>SYMBOL</td>
                <td>ADDRESS</td>
                <td className={styles.tdRight}>TOTAL SUPPLY</td>
                <td></td>
              </tr>
              {props.issuerInfo.assets.map((item, index) => (
                <tr
                  onClick={(): void => toManagement(item)}
                  className={styles.trContent}
                  key={index}
                >
                  <td>{item.code}</td>
                  <td className={styles.tdIssuer}>
                    {item.issuer}
                    {isReadOnly(item.issuer) && (
                      <CustomTag
                        message="READ ONLY"
                        tooltip="The account used to load the list has only view permission over this asset."
                      />
                    )}
                  </td>
                  <td className={styles.tdRight}>{item.supply}</td>
                  <td>
                    <Button
                      size={Button.size.small}
                      variant={Button.variant.secondary}
                      style={{ width: '70px' }}
                    >
                      {isReadOnly(item.issuer) ? 'View' : 'Manage'}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className={styles.empty}>
            <List size={24} />
            <p>No assets created</p>
          </div>
        )}
      </Card>
    </div>
  )
}

export { ListAssets }
