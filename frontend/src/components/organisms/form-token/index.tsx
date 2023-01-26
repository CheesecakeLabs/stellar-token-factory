import { FunctionComponent, useState } from 'react'
import {
  Button,
  Card,
  Heading6,
  IconButton,
  Input,
  Tooltip,
} from '@stellar/design-system'
import { Info, Key } from 'react-feather'
import { getPublicKey } from '@stellar/freighter-api'
import { CustomError, TokenMessage } from 'components/atoms'

import styles from './styles.module.scss'
import {
  defaultErrors,
  defaultResponseSubmit,
  getInitialAsset,
} from './constants'
import { validateInputError, handleSubmitErrors } from './form-validation'
import { FactoryService } from 'services/factory'
import { FreighterService } from 'services/freighter'

export interface IFormTokenProps {
  publicKey: string
  loadTokens: () => void
}

const FormToken: FunctionComponent<IFormTokenProps> = formTokenProps => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [responseSubmit, setResponseSubmit] = useState(defaultResponseSubmit)
  const [inputs, setInputs] = useState(
    getInitialAsset(formTokenProps.publicKey)
  )
  const [inputsErrors, setInputsErrors] = useState(defaultErrors)

  const handleChange = (event: {
    target: { name: string; value: string }
  }): void => {
    cleanFields(event.target.name)
    const name = event.target.name
    const value = event.target.value
    setInputs(values => ({ ...values, [name]: value }))
  }

  const getKey = async (field: string): Promise<void> => {
    cleanFields(field)
    const publicKey = await getPublicKey()
    setInputs(values => ({ ...values, [field]: publicKey }))
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

    FactoryService.addAsset(
      inputs.issuer,
      inputs.distributor,
      inputs.asset_code,
      inputs.limit
    )
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
        setInputs(getInitialAsset(formTokenProps.publicKey))
        formTokenProps.loadTokens()
      })
      .catch(e => {
        setError(e.response?.data?.message)
      })
  }

  return (
    <Card variant={Card.variant.highlight}>
      <Heading6>Asset forging operation</Heading6>
      <div className={styles.contentForm}>
        <Input
          name="issuer"
          id="input-issuer-account"
          label="Issuer Account"
          placeholder="Address issuer account"
          value={inputs.issuer || ''}
          required
          onChange={handleChange}
          error={inputsErrors.issuer}
          autoComplete="off"
          rightElement={
            <IconButton
              altText="Get Public Key"
              icon={<Key key="key-issuer" />}
              onClick={(): Promise<void> => getKey('issuer')}
            />
          }
        />
        <Input
          name="distributor"
          id="input-distributor-account"
          label="Distribution Account"
          placeholder="Address distribution account"
          required
          value={inputs.distributor || ''}
          onChange={handleChange}
          error={inputsErrors.distributor}
          autoComplete="off"
          rightElement={
            <IconButton
              altText="Get Public Key"
              icon={<Key key="key-distributor" />}
              onClick={(): Promise<void> => getKey('distributor')}
            />
          }
        />
        <div className={styles.displayFields}>
          <div className={styles.symbolField}>
            <Input
              name="asset_code"
              id="input-token-symbol"
              label="Name Your Asset"
              placeholder="Asset Code"
              required
              value={inputs.asset_code || ''}
              error={inputsErrors.asset_code}
              maxLength={12}
              autoComplete="off"
              onChange={handleChange}
            />
          </div>
          <div className={styles.limitField}>
            <Input
              name="limit"
              id="input-total-limit"
              label={
                <label>
                  <Tooltip content="This field is optional, not filling it implies the maximum network limit.">
                    Add a Limit <Info size={14} className={styles.iconLimit} />
                  </Tooltip>
                </label>
              }
              placeholder="Limit of the amount of the asset the distributor can hold"
              type="number"
              required
              value={inputs.limit || ''}
              error={inputsErrors.limit}
              autoComplete="off"
              onChange={handleChange}
            />
          </div>
        </div>
        <div className={styles.submitContent}>
          <Button onClick={handleSubmit} type={'submit'} isLoading={isLoading}>
            Submit
          </Button>
        </div>
        {error ? <CustomError message={error} /> : <div />}
        <TokenMessage
          hash={responseSubmit.transaction_hash}
          link={responseSubmit.transaction_link}
        />
      </div>
    </Card>
  )
}

export { FormToken }
