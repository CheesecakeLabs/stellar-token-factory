import { FunctionComponent, useState } from 'react'
import { Button, Card, Input, Tooltip } from '@stellar/design-system'
import { CustomError, TokenMessage } from 'components/atoms'
import { defaultResponseSubmit } from 'components/organisms/form-token/constants'
import { FactoryService } from 'services/factory'
import { FreighterService } from 'services/freighter'

import styles from './styles.module.scss'
import { getInitialFinancialDetails, financialDetailsErrors } from './constants'
import { handleSubmitErrors, validateInputError } from './form-validation'
import { Info } from 'react-feather'

export interface IFinancialDetailsProps {
  treasury: string
  assetCode: string
  issuer: string
}

const FinancialDetails: FunctionComponent<IFinancialDetailsProps> = props => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [inputs, setInputs] = useState(
    getInitialFinancialDetails(props.treasury)
  )
  const [inputsErrors, setInputsErrors] = useState(financialDetailsErrors)
  const [responseSubmit, setResponseSubmit] = useState(defaultResponseSubmit)

  const handleChange = (event: {
    target: { name: string; value: string }
  }): void => {
    cleanFields(event.target.name)
    const name = event.target.name
    const value = event.target.value
    setInputs(values => ({ ...values, [name]: value }))
  }

  const cleanFields = (field: string): void => {
    setError('')
    setResponseSubmit(defaultResponseSubmit)
    setInputsErrors(values => ({ ...values, [field]: '' }))
  }

  const handleSubmit = async (): Promise<void> => {
    setIsLoading(true)
    setError('')

    if (validateInputError(inputs, setInputsErrors, setError)) {
      setIsLoading(false)
      return
    }

    FactoryService.postFinancialDetails(inputs.name, inputs.value, props.issuer)
      .then(async response => {
        const result = await FreighterService.requestSignatures(response.data)
        await postEnvelopeXdr(result)
      })
      .catch(e => {
        const responseError = e.response?.data
        handleSubmitErrors(
          responseError,
          e.response?.data?.code,
          error,
          setInputsErrors,
          setError
        )
      })
      .finally(() => {
        setIsLoading(false)
      })
  }

  const postEnvelopeXdr = async (xdr: string): Promise<void> => {
    await FactoryService.postEnvelope(xdr)
      .then(async response => {
        setResponseSubmit(response.data)
        setInputs(getInitialFinancialDetails(props.treasury))
      })
      .catch(e => {
        setError(e.response?.data?.message)
      })
  }

  return (
    <Card variant={Card.variant.highlight}>
      <div className={styles.field}>
        <Input
          name="name"
          id="input-name"
          label={
            <label>
              <Tooltip content="If this is a new name it will add the given name/value pair to the account. If this name is already present then the associated value will be modified.">
                Financial Operation Name{' '}
                <Info size={14} className={styles.iconTooltip} />
              </Tooltip>
            </label>
          }
          placeholder="Name"
          value={inputs.name || ''}
          onChange={handleChange}
          error={inputsErrors.name}
          autoComplete="off"
          maxLength={64}
        />
      </div>
      <div className={styles.field}>
        <Input
          name="value"
          id="input-value"
          label={
            <label>
              <Tooltip content="Value is optional. If not present then the existing name will be deleted.">
                Financial Operation Value{' '}
                <Info size={14} className={styles.iconTooltip} />
              </Tooltip>
            </label>
          }
          placeholder="Value (Optional)"
          value={inputs.value || ''}
          onChange={handleChange}
          error={inputsErrors.value}
          autoComplete="off"
          maxLength={64}
        />
      </div>
      <div className={styles.contentSubmit}>
        <Button isLoading={isLoading} onClick={handleSubmit}>
          Submit
        </Button>
      </div>
      {error ? <CustomError message={error} /> : <div />}
      <TokenMessage
        hash={responseSubmit.transaction_hash}
        link={responseSubmit.transaction_link}
      />
    </Card>
  )
}

export { FinancialDetails }
