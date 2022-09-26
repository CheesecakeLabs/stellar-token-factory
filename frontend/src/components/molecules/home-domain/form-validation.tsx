import { Dispatch, SetStateAction } from 'react'
import { messageError } from 'services/factory/constants'
import { defaultHomeDomain, homeDomainErrors } from './constants'

export const validateInputError = (
  inputs: typeof defaultHomeDomain,
  setInputsErrors: Dispatch<SetStateAction<typeof homeDomainErrors>>,
  setError: Dispatch<SetStateAction<string>>
): boolean => {
  let hasError = false
  try {
    if (!inputs.home_domain) {
      hasError = true
      setInputsErrors(values => ({
        ...values,
        ['home_domain']: 'The home domain must be informed',
      }))
    }
  } catch (e) {
    hasError = true
    setError((e as string) || 'There are invalid fields')
  }
  return hasError
}

export const handleSubmitErrors = (
  responseError: typeof homeDomainErrors,
  code: number,
  error: string,
  setInputsErrors: Dispatch<SetStateAction<typeof homeDomainErrors>>,
  setError: Dispatch<SetStateAction<string>>
): void => {
  const defaultMessageError =
    'An error has occurred, please check the information provided.'
  if (code) {
    const error = messageError.get(code)
    setError(error ?? defaultMessageError)
    return
  }
  if (responseError?.home_domain) {
    setInputsErrors(values => ({
      ...values,
      ['home_domain']: responseError.home_domain,
    }))
  }
  if (!error) {
    setError(defaultMessageError)
  }
}
