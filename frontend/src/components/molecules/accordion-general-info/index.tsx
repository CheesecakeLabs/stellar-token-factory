import { Dispatch, FunctionComponent, SetStateAction, useState } from 'react'
import { Button, Input } from '@stellar/design-system'
import { ArrowDown, ArrowUp, Edit, Trash } from 'react-feather'

import styles from './styles.module.scss'
import { inputsGeneralInfo, IToml } from '../generate-toml/constants'

export interface IAccordionGeneralInfoProps {
  toml: IToml
  setToml: Dispatch<SetStateAction<IToml>>
}

const AccordionGeneralInfo: FunctionComponent<
  IAccordionGeneralInfoProps
> = props => {
  const [isActive, setIsActive] = useState(true)
  const [inputs, setInputs] = useState(inputsGeneralInfo)

  const handleChange = (event: {
    target: { name: string; value: string }
  }): void => {
    const name = event.target.name
    const value = event.target.value
    setInputs(values => ({ ...values, [name]: value }))
  }

  const addValue = (): void => {
    props.toml.general_info.accounts = [
      ...props.toml.general_info.accounts,
      inputs.account,
    ]
    props.setToml(props.toml)
    setInputs(values => ({ ...values, ['account']: '' }))
  }

  const removeAccount = (account: number): void => {
    setInputs(values => ({ ...values, ['account']: inputs.account }))
    props.toml.general_info.accounts.splice(account, 1)
    props.setToml(props.toml)
  }

  const editAccount = (account: string): void => {
    setInputs(values => ({ ...values, ['account']: account }))
    props.toml.general_info.accounts = [
      ...props.toml.general_info.accounts.filter(item => item !== account),
    ]
    props.setToml(props.toml)
  }

  return (
    <div>
      <div className={styles.accordion}>
        <div
          className={styles.accordionItem}
          onClick={(): void => setIsActive(!isActive)}
        >
          General Information
          {isActive ? <ArrowDown size={16} /> : <ArrowUp size={16} />}
        </div>
      </div>
      {isActive && (
        <div className={styles.accordionContent}>
          {props.toml.general_info.accounts.map((item, index) => (
            <div className={styles.listData} key={index}>
              {item}
              <div className={styles.listAction}>
                <Edit size={16} onClick={(): void => editAccount(item)} />
                <div className={styles.spacer} />
                <Trash size={16} onClick={(): void => removeAccount(index)} />
              </div>
            </div>
          ))}

          <div className={styles.inputForm}>
            <div className={styles.fieldAccount}>
              <Input
                name="account"
                id="input-account"
                placeholder="Stellar account"
                value={inputs.account || ''}
                onChange={handleChange}
                autoComplete="off"
              />
            </div>
            <Button
              variant={Button.variant.tertiary}
              onClick={addValue}
              disabled={!inputs.account}
            >
              Add
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}

export { AccordionGeneralInfo }
