import { FunctionComponent, useCallback } from 'react'
import { Card, Heading6 } from '@stellar/design-system'
import { CustomLoader, CustomTag } from 'components/atoms'

import styles from './styles.module.scss'
import { useNavigate } from 'react-router-dom'
import { IAssetProps, IIssuerInfo } from 'services/factory/interfaces'
import { List } from 'react-feather'

export interface IListAssetsProps {
  issuerInfo?: IIssuerInfo
  isLoading: boolean
  issuer: string
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
        <Heading6>Tokens</Heading6>
        {props.isLoading ? (
          <CustomLoader />
        ) : props.issuerInfo && props.issuerInfo?.assets.length > 0 ? (
          <table>
            <tbody>
              <tr className={styles.tableHeader}>
                <td>SYMBOL</td>
                <td>ADDRESS</td>
                <td className={styles.tdRight}>TOTAL SUPPLY</td>
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
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className={styles.empty}>
            <List size={24} />
            <p>No tokens created</p>
          </div>
        )}
      </Card>
    </div>
  )
}

export { ListAssets }
