import { Dispatch, FunctionComponent, SetStateAction, useState } from 'react'
import { Button } from '@stellar/design-system'
import { ArrowDown, ArrowUp, Edit, Trash } from 'react-feather'

import styles from './styles.module.scss'
import { ICurrency, inputsCurrencyDoc, IToml } from '../generate-toml/constants'
import { FormCurrencyDoc } from '../form-currency-doc'
import { ConfirmModal } from 'components/atoms'

export interface IAccordionCurrencyDocProps {
  toml: IToml
  setToml: Dispatch<SetStateAction<IToml>>
}

const AccordionCurrencyDoc: FunctionComponent<
  IAccordionCurrencyDocProps
> = props => {
  const [isActive, setIsActive] = useState(true)
  const [values, setValues] = useState(inputsCurrencyDoc)
  const [isModalVisible, setModalVisible] = useState(false)
  const [isModalConfirmVisible, setModalConfirmVisible] = useState(false)
  const [indexDelete, setIndexDelete] = useState(-1)

  const closeModal = (): void => {
    setModalVisible(false)
  }

  const closeModalConfirm = (): void => {
    setModalConfirmVisible(false)
  }

  const openModalConfirm = (index: number): void => {
    setIndexDelete(index)
    setModalConfirmVisible(true)
  }

  const removeCurrency = (): void => {
    setModalConfirmVisible(false)
    props.toml.currency_doc.splice(indexDelete, 1)
    props.setToml(props.toml)
  }

  const addValue = (
    inputs: ICurrency,
    isEdit: boolean,
    oldCurrency: ICurrency
  ): void => {
    if (isEdit) {
      props.toml.currency_doc = [
        ...props.toml.currency_doc.filter(item => item !== oldCurrency),
        inputs,
      ]
      props.setToml(props.toml)
      return
    }
    props.toml.currency_doc = [...props.toml.currency_doc, inputs]
    props.setToml(props.toml)
  }

  const editCurrency = (currency: ICurrency): void => {
    setValues(currency)
    setModalVisible(true)
  }

  const addNewDocumentation = (): void => {
    setValues(inputsCurrencyDoc)
    setModalVisible(true)
  }

  return (
    <div>
      <div className={styles.accordion}>
        <div
          className={styles.accordionItem}
          onClick={(): void => setIsActive(!isActive)}
        >
          Currency Documentation
          {isActive ? <ArrowDown size={16} /> : <ArrowUp size={16} />}
        </div>
      </div>
      {isActive && (
        <div className={styles.accordionContent}>
          {props.toml.currency_doc.map((item, index) => (
            <div className={styles.listData} key={index}>
              {item.name || item.issuer}
              <div className={styles.listAction}>
                <Edit size={16} onClick={(): void => editCurrency(item)} />
                <div className={styles.spacer} />
                <Trash
                  size={16}
                  onClick={(): void => openModalConfirm(index)}
                />
              </div>
            </div>
          ))}

          <div className={styles.inputForm}>
            <Button
              variant={Button.variant.tertiary}
              onClick={addNewDocumentation}
            >
              Add documentation
            </Button>
          </div>
        </div>
      )}
      {isModalVisible && (
        <FormCurrencyDoc
          isModalVisible={isModalVisible}
          closeModal={closeModal}
          addValue={addValue}
          initialValues={values}
        />
      )}
      <ConfirmModal
        isModalVisible={isModalConfirmVisible}
        closeModal={closeModalConfirm}
        submit={removeCurrency}
        message={'Are you sure you want to delete this documentation?'}
      />
    </div>
  )
}

export { AccordionCurrencyDoc }
