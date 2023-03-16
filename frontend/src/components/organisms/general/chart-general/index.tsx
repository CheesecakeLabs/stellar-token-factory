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

export interface IChartGeneralProps {
  label: string
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

const ChartGeneral: FunctionComponent<IChartGeneralProps> = ({ label }) => {
  const [optionFilter, setOptionFilter] = useState<'MONTH' | 'YEAR' | 'ALL'>(
    'MONTH'
  )

  const options = {
    responsive: true,
    scales: {
      x: {
        ticks: {
          color: textColorByTheme(document.body.className),
        },
      },
      y: {
        ticks: {
          color: textColorByTheme(document.body.className),
        },
      },
    },
    plugins: {
      tooltip: {
        bodyColor: textColorByTheme(document.body.className),
      },
      legend: {
        labels: {
          color: textColorByTheme(document.body.className),
        },
      },
      color: {
        color: textColorByTheme(document.body.className),
      },
      title: {
        display: false,
      },
    },
  }

  const labels = [
    '1 Jan',
    '3 Jan',
    '6 Jan',
    '9 Jan',
    '12 Jan',
    '15 Jan',
    '18 Jan',
  ]

  const data = {
    labels,
    datasets: [
      {
        label: 'Total supply',
        data: labels.map(() =>
          faker.datatype.number({ min: -1000, max: 1000 })
        ),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Distributor supply',
        data: labels.map(() =>
          faker.datatype.number({ min: -1000, max: 1000 })
        ),
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
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

export { ChartGeneral }
