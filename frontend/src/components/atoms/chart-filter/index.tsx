import classNames from 'classnames'
import { Dispatch, FunctionComponent, SetStateAction } from 'react'

import styles from './styles.module.scss'

export interface IChartFilterProps {
  option: 'MONTH' | 'YEAR' | 'ALL'
  setOption: Dispatch<SetStateAction<'MONTH' | 'YEAR' | 'ALL'>>
}

const ChartFilter: FunctionComponent<IChartFilterProps> = ({
  option,
  setOption,
}) => {
  return (
    <div className={styles.container}>
      <div
        onClick={(): void => setOption('MONTH')}
        className={classNames(
          styles.button,
          option == 'MONTH' ? styles.selected : undefined
        )}
      >
        1 month
      </div>
      <div
        onClick={(): void => setOption('YEAR')}
        className={classNames(
          styles.button,
          option == 'YEAR' ? styles.selected : undefined
        )}
      >
        1 year
      </div>
      <div
        onClick={(): void => setOption('ALL')}
        className={classNames(
          styles.button,
          option == 'ALL' ? styles.selected : undefined
        )}
      >
        All
      </div>
    </div>
  )
}

export { ChartFilter }
