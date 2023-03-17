import { FunctionComponent } from 'react'
import { Card } from '@stellar/design-system'

import styles from './styles.module.scss'
import { CustomLoader } from 'components/atoms'
import { List } from 'react-feather'
import { IClawbackTransaction } from 'services/factory/interfaces'
import { formatNumber, formatSimpleDate } from 'utils/formatter'

export interface IListClawbackAccountsProps {
  isLoading: boolean
  data: IClawbackTransaction[]
}

const ListClawbackAccounts: FunctionComponent<IListClawbackAccountsProps> = ({
  isLoading,
  data,
}) => {
  return (
    <div className={styles.container}>
      <Card variant={Card.variant.highlight}>
        <div className={styles.label}>Last clawback transactions</div>
        {isLoading ? (
          <CustomLoader />
        ) : data && data.length > 0 ? (
          <table>
            <tbody>
              <tr className={styles.tableHeader}>
                <td>Date</td>
                <td>Amount</td>
                <td>From</td>
              </tr>
              {data.map((item, index) => (
                <tr className={styles.trContent} key={index}>
                  <td>{formatSimpleDate(item.date)}</td>
                  <td>
                    {formatNumber(item.amount)} {item.symbol}
                  </td>
                  <td className={styles.tdAccount}>{item.account}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className={styles.empty}>
            <List size={24} />
            <p>No clawback transactions</p>
          </div>
        )}
      </Card>
    </div>
  )
}

export { ListClawbackAccounts }
