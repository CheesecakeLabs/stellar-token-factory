import { useState } from 'react'

import { InputNumber } from 'antd'

import styles from './styles.module.scss'

export const Amount: React.FC = () => {
  const [amount, setAmount] = useState<number | string | null>()

  const onChange = (value: number | string | null): void => {
    setAmount(value)
  }

  return (
    <div className={styles.container}>
      <InputNumber
        defaultValue={amount ?? ''}
        formatter={(value): string =>
          `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
        }
        parser={(value): string =>
          value ? value.replace(/\$\s?|(,*)/g, '') : ''
        }
        onChange={onChange}
        placeholder={'Payment amount'}
        className={styles.input}
        size={'large'}
      />
    </div>
  )
}
