import { Dispatch, SetStateAction } from 'react'
import { messageError } from 'services/factory/constants'
import { defaultAsset, defaultErrors } from './constants'

export const validateInputError = (
  inputs: typeof defaultAsset,
  setInputsErrors: Dispatch<SetStateAction<typeof defaultErrors>>,
  setError: Dispatch<SetStateAction<string>>
): boolean => {
  let hasError = false
  try {
    if (!inputs.issuer) {
      hasError = true
      setInputsErrors(values => ({
        ...values,
        ['issuer']: 'The issuing address must be informed',
      }))
    }
    if (!inputs.distributor) {
      hasError = true
      setInputsErrors(values => ({
        ...values,
        ['distributor']: 'The distribution address must be informed',
      }))
    }
    if (!inputs.asset_code) {
      hasError = true
      setInputsErrors(values => ({
        ...values,
        ['asset_code']: 'The symbol must be informed',
      }))
    }
    if (inputs.limit && Number(inputs.limit) <= 0) {
      hasError = true
      setInputsErrors(values => ({
        ...values,
        ['limit']: 'If informed, the limit must be greater than zero',
      }))
    }
  } catch (e) {
    hasError = true
    setError((e as string) || 'There are invalid fields')
  }
  return hasError
}

export const handleSubmitErrors = (
  responseError: typeof defaultAsset,
  code: number,
  error: string,
  setError: Dispatch<SetStateAction<string>>
): void => {
  const defaultMessageError =
    'An error has occurred, please check the information provided.'
  if (code) {
    const error = messageError.get(code)
    setError(error ?? defaultMessageError)
    return
  }
  if (responseError?.limit) {
    setError(`Limit: ${responseError.limit}`)
  }
  if (responseError?.issuer) {
    setError(`Issuing account: ${responseError.issuer}`)
  }
  if (responseError?.distributor) {
    setError(`Distribution account: ${responseError.distributor}`)
  }
  if (responseError?.asset_code) {
    setError(`Symbol: ${responseError.asset_code}`)
  }
  setError(error ? error : defaultMessageError)
}
