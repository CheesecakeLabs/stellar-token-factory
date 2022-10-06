import { FunctionComponent, useState } from 'react'
import { Button, Card, IconButton, Input, Toggle } from '@stellar/design-system'
import { CustomError, TokenMessage } from 'components/atoms'
import { getPublicKey } from '@stellar/freighter-api'
import { Info, Key } from 'react-feather'
import { defaultResponseSubmit } from 'components/organisms/form-token/constants'
import { FactoryService } from 'services/factory'
import { FreighterService } from 'services/freighter'

import styles from './styles.module.scss'
import { clawbackErrors, defaultClawback } from './constants'
import { handleSubmitErrors, validateInputError } from './form-validation'
import { UnauthorizedMessage } from 'components/atoms/unauthorized-message'

export interface IClawbackProps {
  distribution: string
  assetCode: string
  issuer: string
  authorized: boolean
}

const Clawback: FunctionComponent<IClawbackProps> = props => {
  const [isClaimableId, setIsClaimableId] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [inputs, setInputs] = useState(defaultClawback)
  const [inputsErrors, setInputsErrors] = useState(clawbackErrors)
  const [responseSubmit, setResponseSubmit] = useState(defaultResponseSubmit)

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

    if (validateInputError(inputs, setInputsErrors, setError, isClaimableId)) {
      setIsLoading(false)
      return
    }

    FactoryService.postClawback(
      props.issuer,
      inputs.target,
      props.assetCode,
      inputs.amount,
      inputs.claimable_id,
      isClaimableId
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
        setInputs(defaultClawback)
      })
      .catch(e => {
        setError(e.response?.data?.message)
      })
  }

  return (
    <Card variant={Card.variant.highlight}>
      {props.authorized ? (
        <div>
          <div className={styles.toogle}>
            <div className={styles.infoClaimable}>
              <Info size={18} className={styles.iconInfo} />
              <p>
                You can also use a Claimable ID.{' '}
                <a
                  href="https://developers.stellar.org/docs/glossary/claimable-balance"
                  target="_blank"
                >
                  {' '}
                  More Info
                </a>
              </p>
            </div>
            <Toggle
              id="toggle-claimable"
              labelOn="Use Claimable ID"
              labelPosition={Toggle.labelPosition.left}
              onChange={function (): void {
                setIsClaimableId(!isClaimableId)
              }}
              checked={isClaimableId}
            />
          </div>
          {isClaimableId ? (
            <div className={styles.fields}>
              <Input
                name="claimable_id"
                id="input-claimable-id"
                label="Claimable ID"
                placeholder="Claimable ID"
                value={inputs.claimable_id || ''}
                onChange={handleChange}
                error={inputsErrors.claimable_id}
                autoComplete="off"
              />
            </div>
          ) : (
            <div>
              <div className={styles.fields}>
                <Input
                  name="amount"
                  id="input-amount"
                  label="Amount"
                  placeholder="Token amount you want to clawback"
                  type="number"
                  value={inputs.amount || ''}
                  onChange={handleChange}
                  error={inputsErrors.amount}
                  autoComplete="off"
                  min={0}
                />
              </div>
              <div className={styles.fieldTarget}>
                <Input
                  name="target"
                  id="input-target"
                  label="Target (Investor / Holder) Address"
                  placeholder="Target"
                  value={inputs.target || ''}
                  onChange={handleChange}
                  error={inputsErrors.target}
                  autoComplete="off"
                  rightElement={
                    <IconButton
                      altText="Get Public Key"
                      icon={<Key key='target-clawback'/>}
                      onClick={(): Promise<void> => getKey('target')}
                    />
                  }
                />
              </div>
            </div>
          )}
          <div className={styles.contentSubmit}>
            <Button isLoading={isLoading} onClick={handleSubmit}>
              Clawback
            </Button>
          </div>
          {error ? <CustomError message={error} /> : <div />}
          <TokenMessage
            hash={responseSubmit.transaction_hash}
            link={responseSubmit.transaction_link}
          />
        </div>
      ) : (
        <UnauthorizedMessage message="You are not authorized to perform Clawback, please check permission in settings" />
      )}
    </Card>
  )
}

export { Clawback }
