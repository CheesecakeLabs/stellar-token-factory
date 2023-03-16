import { FunctionComponent } from 'react'
import { Card } from '@stellar/design-system'

import styles from './styles.module.scss'
import { CustomLoader } from 'components/atoms'
import { List } from 'react-feather'
import { ITopHolders } from 'services/factory/interfaces'

export interface IListHoldersProps {
  isLoading: boolean
  data: ITopHolders[]
}

const ListHolders: FunctionComponent<IListHoldersProps> = ({
  isLoading,
  data,
}) => {
  return (
    <div className={styles.container}>
      <Card variant={Card.variant.highlight}>
        <div className={styles.label}>Top 5 holders</div>
        {isLoading ? (
          <CustomLoader />
        ) : data && data.length > 0 ? (
          <table>
            <tbody>
              <tr className={styles.tableHeader}>
                <td>Account</td>
                <td>Balance</td>
                <td></td>
              </tr>
              {data.map((item, index) => (
                <tr className={styles.trContent} key={index}>
                  <td className={styles.tdAccount}>{item.account}</td>
                  <td className={styles.tdIssuer}>{item.balance} {item.symbol}</td>
                  <td className={styles.tdRight}>{item.percentage}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className={styles.empty}>
            <List size={24} />
            <p>No top holders</p>
          </div>
        )}
      </Card>
    </div>
  )
}

export { ListHolders }
