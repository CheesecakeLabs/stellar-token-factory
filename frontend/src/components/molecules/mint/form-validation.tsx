import { Dispatch, SetStateAction } from 'react'
import { messageError } from 'services/factory/constants'
import { defaultMint, mintErrors } from './constants'

export const validateInputError = (
  inputs: typeof defaultMint,
  setInputsErrors: Dispatch<SetStateAction<typeof mintErrors>>,
  setError: Dispatch<SetStateAction<string>>
): boolean => {
  let hasError = false
  try {
    if (!inputs.amount) {
      hasError = true
      setInputsErrors(values => ({
        ...values,
        ['amount']: 'The amount must be informed',
      }))
    }
    if (!inputs.distributor) {
      hasError = true
      setInputsErrors(values => ({
        ...values,
        ['distributor']: 'The treasury address must be informed',
      }))
    }
  } catch (e) {
    hasError = true
    setError((e as string) || 'There are invalid fields')
  }
  return hasError
}

export const handleSubmitErrors = (
  responseError: typeof mintErrors,
  code: number,
  error: string,
  setInputsErrors: Dispatch<SetStateAction<typeof mintErrors>>,
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
  if (responseError?.distributor) {
    setInputsErrors(values => ({
      ...values,
      ['distributor']: responseError.distributor,
    }))
  }
  if (!error) {
    setError(defaultMessageError)
  }
}
