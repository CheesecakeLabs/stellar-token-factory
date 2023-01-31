import { Dispatch, SetStateAction } from 'react'

import { ConfigProvider, Select } from 'antd'

import {
  InputText,
  InputTextVariant,
  Typography,
  TypographyVariant,
} from 'components/atoms'

import styles from './styles.module.scss'

interface IAmountProps {
  amount: string | undefined
  onChangeText(value: string): void
  payee: Hooks.UsePayeesTypes.IPayee | undefined
  payees: Hooks.UsePayeesTypes.IPayee[] | undefined
  setPayee: Dispatch<SetStateAction<Hooks.UsePayeesTypes.IPayee | undefined>>
  isSelectPayee: boolean
}

export const Amount: React.FC<IAmountProps> = ({
  amount,
  onChangeText,
  payee,
  payees,
  setPayee,
  isSelectPayee,
}) => {
  function onChange(event: React.ChangeEvent<HTMLInputElement>): void {
    let value = event.target.value
    value = value.replace(/\D/g, '')
    value = value.replace(/(\d)(\d{2})$/, '$1.$2')
    value = value.replace(/(?=(\d{3})+(\D))\B/g, ',')

    onChangeText(value)
  }

  const handleChange = (value: string): void => {
    const data = payees?.find(item => item.name == value)
    if (data) setPayee(data)
  }

  return (
    <div className={styles.container}>
      {isSelectPayee && (
        <>
          <Typography
            variant={TypographyVariant.label}
            text={`Select the payee`}
            className={styles.title}
          />
          <ConfigProvider
            theme={{
              token: {
                colorBgContainer: '#ecf2f7',
                borderRadius: 4,
                controlHeight: 48,
                colorBorder: 'none',
                colorTextPlaceholder: '#3e5670',
              },
            }}
          >
            <Select
              showSearch
              placeholder="Search to Select"
              optionFilterProp="children"
              filterOption={(input, option): boolean =>
                (option?.label ?? '').includes(input)
              }
              filterSort={(optionA, optionB): number =>
                (optionA?.label ?? '')
                  .toLowerCase()
                  .localeCompare((optionB?.label ?? '').toLowerCase())
              }
              options={payees?.map(payee => {
                return {
                  value: payee.name,
                  label: payee.name,
                }
              })}
              onChange={handleChange}
              className={styles.select}
            />
          </ConfigProvider>
        </>
      )}
      <Typography
        variant={TypographyVariant.label}
        text={`Amount in USD ${payee ? `destined to pay ${payee?.name}` : ''}`}
        className={styles.title}
      />
      <InputText
        variant={InputTextVariant.tertiary}
        name={'amount'}
        handleChange={(event): void => onChange(event)}
        type={'text'}
        value={amount}
        placeHolder={'0.00'}
        prefix={'$'}
      />
    </div>
  )
}
