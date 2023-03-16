import { FunctionComponent } from 'react'
import { Card } from '@stellar/design-system'

import styles from './styles.module.scss'
import { CustomLoader } from 'components/atoms'
import { List } from 'react-feather'
import { IInfoTransaction } from 'services/factory/interfaces'
import { formatSimpleDate } from 'utils/formatter'

export interface IListTransferTransactionsProps {
  isLoading: boolean
  data: IInfoTransaction[]
}

const ListTransferTransactions: FunctionComponent<IListTransferTransactionsProps> = ({
  isLoading,
  data,
}) => {
  return (
    <div className={styles.container}>
      <Card variant={Card.variant.highlight}>
        <div className={styles.label}>Last Mint transactions</div>
        {isLoading ? (
          <CustomLoader />
        ) : data && data.length > 0 ? (
          <table>
            <tbody>
              <tr className={styles.tableHeader}>
                <td>Date</td>
                <td>Amount</td>
                <td>Hash</td>
              </tr>
              {data.map((item, index) => (
                <tr className={styles.trContent} key={index}>
                  <td>{formatSimpleDate(item.date)}</td>
                  <td>
                    {item.amount} {item.symbol}
                  </td>
                  <td className={styles.tdHash}>{item.hash}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className={styles.empty}>
            <List size={24} />
            <p>No transactions</p>
          </div>
        )}
      </Card>
    </div>
  )
}

export { ListTransferTransactions }
