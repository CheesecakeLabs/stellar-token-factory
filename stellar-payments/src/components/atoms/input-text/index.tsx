import classNames from 'classnames'

import styles from './styles.module.scss'

export enum InputTextVariant {
  primary = 'primary',
  secondary = 'secondary',
}

export interface IInputProps {
  variant: InputTextVariant
  name: string
  handleChange: (event: { target: { name: string; value: string } }) => void
  value?: string
  type?: string
  padding?: string
  maxLength?: number
  placeHolder?: string
}

const InputText = (props: IInputProps): JSX.Element => {
  return (
    <div className={classNames(styles.inputContainer, styles[props.variant])}>
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
