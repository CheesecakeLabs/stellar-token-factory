import { Dispatch, SetStateAction } from 'react'
import { messageError } from 'services/factory/constants'
import { defaultClawback, clawbackErrors } from './constants'

export const validateInputError = (
  inputs: typeof defaultClawback,
  setInputsErrors: Dispatch<SetStateAction<typeof clawbackErrors>>,
  setError: Dispatch<SetStateAction<string>>,
  isClaimableId: boolean
): boolean => {
  let hasError = false
  try {
    if (!isClaimableId && !inputs.amount) {
      hasError = true
      setInputsErrors(values => ({
        ...values,
        ['amount']: 'The amount must be informed',
      }))
    }
    if (!isClaimableId && !inputs.target) {
      hasError = true
      setInputsErrors(values => ({
        ...values,
        ['target']: 'The target must be informed',
      }))
    }
    if (isClaimableId && !inputs.claimable_id) {
      hasError = true
      setInputsErrors(values => ({
        ...values,
        ['claimable_id']: 'The Claimable ID must be informed',
      }))
    }
  } catch (e) {
    hasError = true
    setError((e as string) || 'There are invalid fields')
  }
  return hasError
}

export const handleSubmitErrors = (
  responseError: typeof clawbackErrors,
  code: number,
  error: string,
  setInputsErrors: Dispatch<SetStateAction<typeof clawbackErrors>>,
  setError: Dispatch<SetStateAction<string>>
): void => {
  const defaultMessageError =
    'An error has occurred, please check the information provided.'
  if (code) {
    const error = messageError.get(code)
    setError(error ?? defaultMessageError)
    return
  }
  if (responseError?.amount) {
    setInputsErrors(values => ({ ...values, ['amount']: responseError.amount }))
  }
  if (responseError?.target) {
    setInputsErrors(values => ({ ...values, ['target']: responseError.target }))
  }
  if (responseError?.claimable_id) {
    setInputsErrors(values => ({
      ...values,
      ['claimable_id']: responseError.claimable_id,
    }))
  }
  if (!error) {
    setError(defaultMessageError)
  }
}
