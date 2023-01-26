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
  payee: Hooks.UsePayeesTypes.IPayee
}

export const Amount: React.FC<IAmountProps> = ({
  amount,
  onChangeText,
  payee,
}) => {
  function onChange(event: React.ChangeEvent<HTMLInputElement>): void {
    let value = event.target.value
    value = value.replace(/\D/g, '')
    value = value.replace(/(\d)(\d{2})$/, '$1.$2')
    value = value.replace(/(?=(\d{3})+(\D))\B/g, ',')

    onChangeText(value)
  }

  return (
    <div className={styles.container}>
      <Typography
        variant={TypographyVariant.label}
        text={`Amount in USD destined to pay ${payee.name}`}
        className={styles.title}
      />
      <InputText
        variant={InputTextVariant.primary}
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
