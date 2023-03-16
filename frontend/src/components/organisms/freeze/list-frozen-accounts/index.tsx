import { FunctionComponent } from 'react'
import { Card } from '@stellar/design-system'

import styles from './styles.module.scss'
import { CustomLoader } from 'components/atoms'
import { List } from 'react-feather'
import { IFrozenAccount } from 'services/factory/interfaces'
import { formatSimpleDate } from 'utils/formatter'

export interface IListFrozenAccountsProps {
  isLoading: boolean
  data: IFrozenAccount[]
}

const ListFrozenAccounts: FunctionComponent<IListFrozenAccountsProps> = ({
  isLoading,
  data,
}) => {
  return (
    <div className={styles.container}>
      <Card variant={Card.variant.highlight}>
        <div className={styles.label}>Frozen accounts</div>
        {isLoading ? (
          <CustomLoader />
        ) : data && data.length > 0 ? (
          <table>
            <tbody>
              <tr className={styles.tableHeader}>
                <td>Freeze Date</td>
                <td>Account</td>
              </tr>
              {data.map((item, index) => (
                <tr className={styles.trContent} key={index}>
                  <td>{formatSimpleDate(item.date_freeze)}</td>
                  <td className={styles.tdAccount}>{item.account}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className={styles.empty}>
            <List size={24} />
            <p>No frozen accounts</p>
          </div>
        )}
      </Card>
    </div>
  )
}

export { ListFrozenAccounts }
