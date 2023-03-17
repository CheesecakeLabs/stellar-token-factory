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
import { Line } from 'react-chartjs-2'
import { faker } from '@faker-js/faker'

import styles from './styles.module.scss'
import { textColorByTheme } from 'services/theme-utils'
import { ChartFilter } from 'components/atoms'
import { labelsChart } from 'utils/chart-utils'

export interface IChartMintProps {
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

const ChartMint: FunctionComponent<IChartMintProps> = ({
  label,
  isDarkMode,
}) => {
  const [optionFilter, setOptionFilter] = useState<'MONTH' | 'YEAR' | 'ALL'>(
    'MONTH'
  )

  const options = {
    responsive: true,
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
  }

  const data = {
    labels: labelsChart(optionFilter),
    datasets: [
      {
        label: 'Minted amount',
        data: labelsChart(optionFilter).map(() =>
          faker.datatype.number({ min: 0, max: 1000 })
        ),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
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
        <Line options={options} data={data} className={styles.chart} />
      </Card>
    </div>
  )
}

export { ChartMint }
