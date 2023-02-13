import { Dispatch, FunctionComponent, SetStateAction, useState } from 'react'
import { Button, Card, Input } from '@stellar/design-system'
import {
  CustomError,
  FabHelper,
  FabHelperVariant,
  TokenMessage,
} from 'components/atoms'
import { defaultResponseSubmit } from 'components/organisms/form-token/constants'
import { FactoryService } from 'services/factory'
import { FreighterService } from 'services/freighter'

import styles from './styles.module.scss'
import { defaultHomeDomain, homeDomainErrors } from './constants'
import { handleSubmitErrors, validateInputError } from './form-validation'
import { TabsManagementEnum } from 'components/templates'

export interface IHomeDomainProps {
  issuer: string
  setShowHelper: Dispatch<SetStateAction<TabsManagementEnum | undefined>>
}

const HomeDomain: FunctionComponent<IHomeDomainProps> = props => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [inputs, setInputs] = useState(defaultHomeDomain)
  const [inputsErrors, setInputsErrors] = useState(homeDomainErrors)
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

    FactoryService.postHomeDomain(inputs.home_domain, props.issuer)
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
        setInputs(defaultHomeDomain)
      })
      .catch(e => {
        setError(e.response?.data?.message)
      })
  }

  return (
    <Card variant={Card.variant.highlight}>
      {false && (
        <FabHelper
          onClick={(): void =>
            props.setShowHelper(TabsManagementEnum.HOME_DOMAIN)
          }
          variant={FabHelperVariant.fixedRight}
        />
      )}
      <Input
        name="home_domain"
        id="input-home_domain"
        label="Home Domain"
        placeholder="Home Domain"
        value={inputs.home_domain || ''}
        onChange={handleChange}
        error={inputsErrors.home_domain}
        autoComplete="off"
      />
      <div className={styles.contentSubmit}>
        <Button isLoading={isLoading} onClick={handleSubmit}>
          Set Home Domain
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

export { HomeDomain }
