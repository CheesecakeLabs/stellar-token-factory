import { FunctionComponent, useState } from 'react'
import { Card } from '@stellar/design-system'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Chart } from 'react-chartjs-2'
import { faker } from '@faker-js/faker'

import 'chart.js/auto'

import styles from './styles.module.scss'
import { textColorByTheme } from 'services/theme-utils'
import { ChartFilter } from 'components/atoms'
import { labelsChart } from 'utils/chart-utils'

export interface IChartTransferProps {
  label: string
  isDarkMode: boolean | undefined
}

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const ChartTransfer: FunctionComponent<IChartTransferProps> = ({
  label,
  isDarkMode,
}) => {
  const [optionFilter, setOptionFilter] = useState<'MONTH' | 'YEAR' | 'ALL'>(
    'MONTH'
  )

  const options = {
    responsive: true,
    plugins: {
      tooltip: {
        bodyColor: textColorByTheme(isDarkMode),
      },
      legend: {
        display: false,
        labels: {
          color: textColorByTheme(isDarkMode),
        },
      },
      color: {
        color: textColorByTheme(isDarkMode),
      },
      title: {
        display: false,
      },
    },
    scales: {
      x: {
        ticks: {
          color: textColorByTheme(isDarkMode),
        },
      },
      y: {
        ticks: {
          color: textColorByTheme(isDarkMode),
        },
      },
    },
  }

  const data = {
    labels: labelsChart(optionFilter),
    datasets: [
      {
        label: 'Amount',
        data: labelsChart(optionFilter).map(() =>
          faker.datatype.number({ min: 0, max: 1000 })
        ),
        borderColor: 'rgb(56,147,138)',
        backgroundColor: 'rgba(56,147,138,0.5)',
        order: 1,
      },
      {
        label: 'Volume',
        data: labelsChart(optionFilter).map(() =>
          faker.datatype.number({ min: 0, max: 1000 })
        ),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        type: 'line' as never,
        order: 0,
      },
    ],
  }

  return (
    <div className={styles.container}>
      <Card variant={Card.variant.highlight}>
        <div className={styles.header}>
          <div className={styles.label}>{label}</div>
          <ChartFilter option={optionFilter} setOption={setOptionFilter} />
        </div>
        <Chart
          type="bar"
          options={options}
          data={data}
          className={styles.chart}
        />
      </Card>
    </div>
  )
}

export { ChartTransfer }
