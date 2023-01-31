import { ChangeEventHandler } from 'react'

import classNames from 'classnames'

import { Typography, TypographyVariant } from '../typography'
import styles from './styles.module.scss'

export enum InputTextVariant {
  primary = 'primary',
  secondary = 'secondary',
  tertiary = 'tertiary',
}

export interface IInputProps {
  variant: InputTextVariant
  name: string
  handleChange: ChangeEventHandler<HTMLInputElement>
  value?: string
  type?: string
  padding?: string
  maxLength?: number
  placeHolder?: string
  prefix?: string
}

const InputText = (props: IInputProps): JSX.Element => {
  return (
    <div className={classNames(styles.inputContainer, styles[props.variant])}>
      {props.prefix && (
        <Typography
          variant={TypographyVariant.label}
          text={props.prefix}
          className={styles.prefix}
        />
      )}
      <input
        name={props.name}
        type={props.type}
        onChange={props.handleChange}
        autoComplete="off"
        value={props.value}
        style={props.padding ? { padding: props.padding } : undefined}
        maxLength={props.maxLength}
        placeholder={props.placeHolder}
      />
    </div>
  )
}

export { InputText }
