import { Dispatch, FunctionComponent, SetStateAction, useState } from 'react'
import { Button, Input } from '@stellar/design-system'
import { ArrowDown, ArrowUp, Edit, Trash } from 'react-feather'

import styles from './styles.module.scss'
import { IContact, inputsContact, IToml } from '../../organisms/generate-toml/constants'

export interface IAccordionContactProps {
  toml: IToml
  setToml: Dispatch<SetStateAction<IToml>>
}

const AccordionContact: FunctionComponent<IAccordionContactProps> = props => {
  const [isActive, setIsActive] = useState(true)
  const [inputs, setInputs] = useState(inputsContact)

  const handleChange = (event: {
    target: { name: string; value: string }
  }): void => {
    const name = event.target.name
    const value = event.target.value
    setInputs(values => ({ ...values, [name]: value }))
  }

  const addValue = (): void => {
    props.toml.point_of_contact_doc = [
      ...props.toml.point_of_contact_doc,
      { name: inputs.name, email: inputs.email },
    ]
    props.setToml(props.toml)
    setInputs(inputsContact)
  }

  const removeContact = (contact: number): void => {
    setInputs(values => ({ ...values, ['name']: inputs.name }))
    props.toml.point_of_contact_doc.splice(contact, 1)
    props.setToml(props.toml)
  }

  const editContact = (contact: IContact): void => {
    setInputs(contact)
    props.toml.point_of_contact_doc = [
      ...props.toml.point_of_contact_doc.filter(item => item !== contact),
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
          Point of contact
          {isActive ? <ArrowDown size={16} /> : <ArrowUp size={16} />}
        </div>
      </div>
      {isActive && (
        <div className={styles.accordionContent}>
          {props.toml.point_of_contact_doc.map((item, index) => (
            <div className={styles.listData} key={index}>
              <div className={styles.listValues}>
                <span>{item.name}</span>
                <span>{item.email}</span>
              </div>
              <div className={styles.listAction}>
                <Edit size={16} onClick={(): void => editContact(item)} />
                <div className={styles.spacerAction} />
                <Trash size={16} onClick={(): void => removeContact(index)} />
              </div>
            </div>
          ))}

          <div className={styles.inputForm}>
            <div className={styles.form}>
              <Input
                name="name"
                id="input-name"
                placeholder="Name"
                value={inputs.name || ''}
                onChange={handleChange}
                autoComplete="off"
              />
              <div className={styles.spacerAction} />
              <Input
                name="email"
                id="input-email"
                placeholder="Email"
                value={inputs.email || ''}
                onChange={handleChange}
                autoComplete="off"
              />
            </div>
            <Button
              variant={Button.variant.tertiary}
              onClick={addValue}
              disabled={!inputs.name.trim() || !inputs.email.trim()}
            >
              Add
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}

export { AccordionContact }
